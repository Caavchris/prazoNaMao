import React from 'react'
import { Publication } from '../types/cnj'

type Props = {
  item: Publication
  onClose: () => void
}

export default function ProcessModal({ item, onClose }: Props) {
  const publicationText = item.texto ?? item.resumo ?? item.ementa ?? item.summary ?? '—'
  const date = item.data_disponibilizacao ?? item.datadisponibilizacao ?? item.dataPublicacao ?? item.data ?? item.publicationDate ?? ''

  const rawLawyers = item.destinatarioadvogados ?? item.advogados ?? item.lawyers ?? item.destinatarios ?? []
  const lawyers = Array.isArray(rawLawyers)
    ? rawLawyers.map((d: any) => {
        const adv = d.advogado ?? d
        return {
          nome: adv.nome ?? adv.name ?? d.nome ?? d,
          oab: adv.numero_oab ?? adv.numeroOab ?? adv.oab ?? (adv.uf_oab && adv.numero_oab ? `${adv.numero_oab}/${adv.uf_oab}` : adv.numero_oab ?? undefined)
        }
      })
    : []

  const tribunal = item.siglaTribunal ?? item.tribunal ?? ''
  const orgao = item.nomeOrgao ?? item.nome_orgao ?? item.nomeOrgao ?? ''
  const tipo = item.tipoComunicacao ?? item.tipo_comunicacao ?? item.tipoComunicacao ?? ''

  const days_left = typeof item.days_left === 'number' ? item.days_left : null
  const status = item.deadline_status ?? 'unknown'
  const badge = () => {
    if (status === 'expired') return { text: `Vencido (${Math.abs(days_left ?? 0)}d)`, className: 'bg-red-100 text-red-700' }
    if (status === 'approaching') return { text: `Próximo (${days_left}d)`, className: 'bg-yellow-100 text-yellow-800' }
    if (status === 'ok') return { text: `OK (${days_left}d)`, className: 'bg-green-100 text-green-800' }
    return { text: '—', className: 'bg-gray-100 text-gray-600' }
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      <div className="absolute inset-0 bg-black opacity-40" onClick={onClose} />
      <div className="relative bg-white rounded shadow-lg w-full max-w-3xl mx-4 p-6 z-10 overflow-auto max-h-[80vh]">
        <div className="flex justify-between items-start">
          <h2 className="text-xl font-bold">Detalhes do processo</h2>
          <button onClick={onClose} className="text-gray-600">Fechar</button>
        </div>

        <div className="mt-4 space-y-3 text-sm text-gray-800">
          <div className="flex items-center gap-4">
            <div><strong>Número do processo:</strong> {item.numero_processo ?? item.numeroProcesso ?? item.processNumber ?? item.numero_processo ?? item.numeroprocessocommascara ?? '—'}</div>
            <div className={`${badge().className} px-2 py-1 rounded text-sm`}>{badge().text}</div>
          </div>
          <div><strong>Data:</strong> {date}</div>
          <div><strong>Órgão:</strong> {orgao} <span className="text-gray-500">{tribunal}</span></div>
          <div><strong>Tipo:</strong> {tipo}</div>

          <div>
            <strong>Advogado(s):</strong>
            {lawyers.length > 0 ? (
              <ul className="list-disc list-inside mt-1">
                {lawyers.map((l: any, idx: number) => (
                  <li key={idx}>{(l.nome ?? l) + (l.oab ? ` — OAB ${l.oab}` : '')}</li>
                ))}
              </ul>
            ) : (
              <span className="ml-1">{item.nomeAdvogado ?? item.lawyerName ?? '—'}</span>
            )}
          </div>

          <div>
            <strong>Texto da publicação:</strong>
            <div className="mt-1 whitespace-pre-wrap text-gray-700">{publicationText}</div>
          </div>

          {item.link && (
            <div>
              <a className="text-blue-600 underline" href={item.link} target="_blank" rel="noreferrer">Abrir processo completo</a>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
