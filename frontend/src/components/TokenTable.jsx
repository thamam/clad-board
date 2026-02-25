function formatNumber(n) {
  if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(1)}M`;
  if (n >= 1_000) return `${(n / 1_000).toFixed(1)}K`;
  return n.toString();
}

export default function TokenTable({ tokenUsage }) {
  if (!tokenUsage || tokenUsage.length === 0) {
    return <p className="text-sm text-gray-400">No token usage data</p>;
  }

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-left text-sm">
        <thead>
          <tr className="border-b border-gray-700 text-gray-400">
            <th className="pb-2 pr-4">Model</th>
            <th className="pb-2 pr-4" colSpan={2}>All Time</th>
            <th className="pb-2 pr-4" colSpan={2}>Last 24h</th>
            <th className="pb-2" colSpan={2}>Month-to-Date</th>
          </tr>
          <tr className="border-b border-gray-700 text-xs text-gray-500">
            <th className="pb-2 pr-4"></th>
            <th className="pb-2 pr-2 font-normal">In</th>
            <th className="pb-2 pr-4 font-normal">Out</th>
            <th className="pb-2 pr-2 font-normal">In</th>
            <th className="pb-2 pr-4 font-normal">Out</th>
            <th className="pb-2 pr-2 font-normal">In</th>
            <th className="pb-2 font-normal">Out</th>
          </tr>
        </thead>
        <tbody>
          {tokenUsage.map((row) => (
            <tr key={row.model} className="border-b border-gray-800 text-gray-300">
              <td className="py-2 pr-4 font-medium text-white">{row.model}</td>
              <td className="py-2 pr-2">{formatNumber(row.all_time_in)}</td>
              <td className="py-2 pr-4">{formatNumber(row.all_time_out)}</td>
              <td className="py-2 pr-2">{formatNumber(row.last_24h_in)}</td>
              <td className="py-2 pr-4">{formatNumber(row.last_24h_out)}</td>
              <td className="py-2 pr-2">{formatNumber(row.mtd_in)}</td>
              <td className="py-2">{formatNumber(row.mtd_out)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
