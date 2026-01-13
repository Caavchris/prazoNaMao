import React from 'react'
import { useQuery } from '@tanstack/react-query'
import { searchDeadlines } from '../api/cnj'
import ResultItem from './ResultItem'

type Props = { lawyerName: string }

export default function ResultsList({ lawyerName }: Props) {
  const enabled = lawyerName.length > 0
  const [autoRefresh, setAutoRefresh] = React.useState(false)
  const [statusApproaching, setStatusApproaching] = React.useState(false)
  const [statusExpired, setStatusExpired] = React.useState(false)
  const [statusOk, setStatusOk] = React.useState(false)

  const statuses = React.useMemo(() => {
    const s: string[] = []
    if (statusApproaching) s.push('approaching')
    if (statusExpired) s.push('expired')
    if (statusOk) s.push('ok')
    return s
  }, [statusApproaching, statusExpired, statusOk])

  const { data, isLoading, isError, refetch } = useQuery(
    ['lawyer-deadlines', lawyerName, statuses],
    () => searchDeadlines(lawyerName, statuses.length ? statuses : undefined),
    { enabled, staleTime: 1000 * 60, retry: 1, refetchInterval: autoRefresh ? 30000 : false }
  )

  if (!enabled) return <div className="text-gray-600">Digite o nome do advogado e clique buscar.</div>
  if (isLoading) return <div className="animate-pulse space-y-2">{[0,1,2].map(i=><div key={i} className="h-20 bg-white rounded shadow p-2" />)}</div>
  if (isError) return <div className="text-red-600">Erro ao carregar resultados. <button onClick={() => refetch()} className="ml-2 text-blue-600 underline">Tentar novamente</button></div>

  const items = Array.isArray(data) ? data : (data?.items ?? [])

  if (!items || items.length === 0) return <div className="text-gray-600">Nenhuma publicação encontrada.</div>

  return (
    <div className="space-y-2 mt-4">
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center gap-3">
          <div className="text-sm text-gray-600">Resultados: {items.length}</div>
          <div className="flex items-center gap-2">
            <label className="flex items-center gap-1 text-sm"><input type="checkbox" checked={statusApproaching} onChange={(e) => setStatusApproaching(e.target.checked)} /> Próximos</label>
            <label className="flex items-center gap-1 text-sm"><input type="checkbox" checked={statusExpired} onChange={(e) => setStatusExpired(e.target.checked)} /> Vencidos</label>
            <label className="flex items-center gap-1 text-sm"><input type="checkbox" checked={statusOk} onChange={(e) => setStatusOk(e.target.checked)} /> OK</label>
          </div>
        </div> 
        <label className="flex items-center gap-2 text-sm">
          <input type="checkbox" checked={autoRefresh} onChange={(e) => setAutoRefresh(e.target.checked)} />
          Auto-refresh (30s)
        </label>
      </div>
      {items.map((item: any, idx: number) => <ResultItem key={idx} item={item} />)}
    </div>
  )
}
