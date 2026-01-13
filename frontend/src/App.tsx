import React, { useState } from 'react'
import SearchBar from './components/SearchBar'
import ResultsList from './components/ResultsList'

export default function App() {
  const [query, setQuery] = useState('')
  return (
    <div className="min-h-screen p-4">
      <div className="max-w-3xl mx-auto">
        <h1 className="text-2xl font-bold mb-4">PrazoNaMão — Consulta por Advogado</h1>
        <SearchBar onSearch={setQuery} />
        <ResultsList lawyerName={query} />
      </div>
    </div>
  )
}
