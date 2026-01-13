import React, { useState } from 'react'

type Props = { onSearch: (s: string) => void }

export default function SearchBar({ onSearch }: Props) {
  const [value, setValue] = useState('')
  return (
    <form onSubmit={(e) => { e.preventDefault(); onSearch(value.trim()) }} className="mb-4 flex gap-2">
      <input
        className="flex-1 p-2 border rounded"
        placeholder="Nome do advogado (ex.: Silva)"
        value={value}
        onChange={(e) => setValue(e.target.value)}
      />
      <button className="px-4 py-2 bg-blue-600 text-white rounded" type="submit">Buscar</button>
    </form>
  )
}
