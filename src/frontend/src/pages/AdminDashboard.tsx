import { useEffect, useState } from 'react'
import { apiGet } from '@/api/client'
import type { AdminStats, AuditLogEntry } from '@/types'

export function AdminDashboard() {
  const [stats, setStats] = useState<AdminStats | null>(null)
  const [auditLogs, setAuditLogs] = useState<AuditLogEntry[]>([])
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let cancelled = false

    Promise.all([
      apiGet<AdminStats>('/api/admin/stats'),
      apiGet<AuditLogEntry[]>('/api/admin/audit-logs?limit=50&offset=0'),
    ])
      .then(([s, logs]) => {
        if (!cancelled) {
          setStats(s)
          setAuditLogs(logs)
        }
      })
      .catch(() => {
        if (!cancelled) setError('Failed to load admin data. Admin access required.')
      })
      .finally(() => {
        if (!cancelled) setLoading(false)
      })

    return () => {
      cancelled = true
    }
  }, [])

  if (loading) {
    return (
      <div className="space-y-6">
        <h1 className="text-2xl font-semibold text-soft-navy">Admin dashboard</h1>
        <p className="text-soft-slate">Loading…</p>
      </div>
    )
  }

  if (error) {
    return (
      <div className="space-y-6">
        <h1 className="text-2xl font-semibold text-soft-navy">Admin dashboard</h1>
        <div className="rounded-xl border border-soft-sage/40 bg-white/60 p-6 shadow-sm">
          <p className="text-red-600" role="alert">
            {error}
          </p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-8">
      <h1 className="text-2xl font-semibold text-soft-navy">Admin dashboard</h1>

      {/* Key metrics */}
      {stats && (
        <section aria-label="Activity metrics">
          <h2 className="text-lg font-medium text-soft-slate mb-3">Activity metrics</h2>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            <div className="rounded-xl border border-soft-sage/40 bg-white/60 p-4 shadow-sm">
              <p className="text-sm text-soft-slate">Users</p>
              <p className="text-2xl font-semibold text-soft-navy">{stats.total_users}</p>
            </div>
            <div className="rounded-xl border border-soft-sage/40 bg-white/60 p-4 shadow-sm">
              <p className="text-sm text-soft-slate">Videos</p>
              <p className="text-2xl font-semibold text-soft-navy">{stats.total_videos}</p>
            </div>
            <div className="rounded-xl border border-soft-sage/40 bg-white/60 p-4 shadow-sm">
              <p className="text-sm text-soft-slate">Detection results</p>
              <p className="text-2xl font-semibold text-soft-navy">{stats.total_results}</p>
            </div>
            <div className="rounded-xl border border-soft-sage/40 bg-white/60 p-4 shadow-sm">
              <p className="text-sm text-soft-slate">Audit log entries</p>
              <p className="text-2xl font-semibold text-soft-navy">{stats.total_audit_logs}</p>
            </div>
          </div>
        </section>
      )}

      {/* Recent audit logs */}
      <section aria-label="Recent audit logs">
        <h2 className="text-lg font-medium text-soft-slate mb-3">Recent audit logs</h2>
        <div className="rounded-xl border border-soft-sage/40 bg-white/60 shadow-sm overflow-hidden">
          {auditLogs.length === 0 ? (
            <div className="p-6 text-soft-slate">No audit log entries yet.</div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-soft-sage/40 bg-soft-sand/40">
                    <th scope="col" className="text-left px-4 py-2 font-medium text-soft-navy">Time</th>
                    <th scope="col" className="text-left px-4 py-2 font-medium text-soft-navy">Action</th>
                    <th scope="col" className="text-left px-4 py-2 font-medium text-soft-navy">User</th>
                    <th scope="col" className="text-left px-4 py-2 font-medium text-soft-navy">Entity</th>
                    <th scope="col" className="text-left px-4 py-2 font-medium text-soft-navy">Details</th>
                  </tr>
                </thead>
                <tbody>
                  {auditLogs.map((log) => (
                    <tr key={log.id} className="border-b border-soft-sage/20">
                      <td className="px-4 py-2 text-soft-slate whitespace-nowrap">
                        {log.created_at ? new Date(log.created_at).toLocaleString() : '—'}
                      </td>
                      <td className="px-4 py-2 text-soft-navy">{log.action}</td>
                      <td className="px-4 py-2 text-soft-slate">{log.username ?? (log.user_id != null ? `#${log.user_id}` : '—')}</td>
                      <td className="px-4 py-2 text-soft-slate">
                        {log.entity_type != null ? `${log.entity_type}${log.entity_id != null ? ` #${log.entity_id}` : ''}` : '—'}
                      </td>
                      <td className="px-4 py-2 text-soft-slate max-w-xs truncate" title={log.details ?? undefined}>
                        {log.details ?? '—'}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </section>
    </div>
  )
}
