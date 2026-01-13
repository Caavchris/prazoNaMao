export interface Publication {
  numeroProcesso?: string
  processNumber?: string
  dataPublicacao?: string
  data?: string
  publicationDate?: string
  resumo?: string
  ementa?: string
  summary?: string
  texto?: string
  link?: string
  nomeAdvogado?: string
  lawyerName?: string
  advogados?: Array<any>
  lawyers?: Array<any>
  // extensão genérica para outros campos
  [key: string]: any
}
