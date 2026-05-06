"use client"

import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Cell } from 'recharts'

interface ChartProps {
  data: any[]
}

export function ScoreDistributionChart({ data }: ChartProps) {
  const chartData = data.map(d => ({
    name: d.name.split(' ')[0],
    score: parseFloat((d.score * 100).toFixed(1))
  }))

  return (
    <div className="w-full h-64 bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-6 shadow-xl">
      <h3 className="text-white/80 font-medium mb-4">Candidate Score Distribution</h3>
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={chartData} margin={{ top: 0, right: 0, left: -20, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#ffffff1a" vertical={false} />
          <XAxis dataKey="name" stroke="#ffffff80" fontSize={12} tickLine={false} axisLine={false} />
          <YAxis stroke="#ffffff80" fontSize={12} tickLine={false} axisLine={false} />
          <Tooltip 
            cursor={{ fill: '#ffffff1a' }}
            contentStyle={{ backgroundColor: '#1a1b26', border: '1px solid #ffffff1a', borderRadius: '8px' }}
            itemStyle={{ color: '#fff' }}
          />
          <Bar dataKey="score" radius={[4, 4, 0, 0]}>
            {chartData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.score > 70 ? '#10b981' : entry.score > 50 ? '#f59e0b' : '#ef4444'} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}
