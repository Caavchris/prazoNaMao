import React from 'react'
import ProcessModal from './ProcessModal'

export default function ResultItem({ item } : { item: any }) {
  const date = item.data_disponibilizacao ?? item.datadisponibilizacao ?? item.dataPublicacao ?? item.data ?? item.publicationDate ?? ''
  const [open, setOpen] = React.useState(false)

  const status = item.deadline_status ?? 'unknown'
  const days_left = typeof item.days_left === 'number' ? item.days_left : null
  const getBadge = () => {
    if (status === 'expired') return { text: `Vencido (${Math.abs(days_left ?? 0)}d)`, color: 'bg-red-100 text-red-700' }
    if (status === 'approaching') return { text: `Próximo (${days_left}d)`, color: 'bg-yellow-100 text-yellow-800' }
    if (status === 'ok') return { text: `OK (${days_left}d)`, color: 'bg-green-100 text-green-800' }
    return { text: '—', color: 'bg-gray-100 text-gray-600' }
  }
  const badge = getBadge()

  return (
    <div className="bg-white rounded shadow p-3">
      <div className="flex items-start justify-between">
        <div className="text-sm text-gray-500">{date}</div>
        <div className={`px-2 py-1 text-xs rounded ${badge.color}`}>{badge.text}</div>
      </div>

      <div className="font-semibold">{item.numero_processo ?? item.numeroProcesso ?? item.processNumber ?? ''}</div>
      <div className="text-gray-700 mt-1">{item.resumo ?? item.ementa ?? item.summary ?? item.texto ?? '—'}</div>

      <div className="mt-3 flex gap-2">
        <button className="px-3 py-1 bg-gray-100 rounded text-sm" onClick={() => setOpen(true)}>Ver detalhes</button>
        {item.link && <a className="px-3 py-1 bg-blue-50 rounded text-sm text-blue-600" href={item.link} target="_blank" rel="noreferrer">Abrir original</a>}
      </div>

      {open && <ProcessModal item={item} onClose={() => setOpen(false)} />}
    </div>
  )
}
