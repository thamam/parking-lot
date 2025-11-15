import Link from 'next/link'

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800">
      <div className="container mx-auto px-4 py-16">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-5xl font-bold mb-6 text-gray-900 dark:text-white">
            Multi-Project Dashboard
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-300 mb-8">
            Manage all your GitHub repositories and research in one place
          </p>

          <div className="grid md:grid-cols-2 gap-6 mt-12">
            <Link href="/dashboard" className="card hover:shadow-lg transition-shadow">
              <h2 className="text-2xl font-semibold mb-3 text-gray-900 dark:text-white">
                Dashboard
              </h2>
              <p className="text-gray-600 dark:text-gray-400">
                View and manage all your projects with GitHub integration
              </p>
            </Link>

            <Link href="/settings" className="card hover:shadow-lg transition-shadow">
              <h2 className="text-2xl font-semibold mb-3 text-gray-900 dark:text-white">
                Settings
              </h2>
              <p className="text-gray-600 dark:text-gray-400">
                Configure GitHub token and sync preferences
              </p>
            </Link>
          </div>

          <div className="mt-16 p-8 card">
            <h3 className="text-2xl font-semibold mb-4 text-gray-900 dark:text-white">
              Features
            </h3>
            <ul className="grid md:grid-cols-2 gap-4 text-left">
              <li className="flex items-start">
                <span className="text-green-500 mr-2">✓</span>
                <span className="text-gray-700 dark:text-gray-300">GitHub repository syncing</span>
              </li>
              <li className="flex items-start">
                <span className="text-green-500 mr-2">✓</span>
                <span className="text-gray-700 dark:text-gray-300">Track research from AI tools</span>
              </li>
              <li className="flex items-start">
                <span className="text-green-500 mr-2">✓</span>
                <span className="text-gray-700 dark:text-gray-300">Project status tracking</span>
              </li>
              <li className="flex items-start">
                <span className="text-green-500 mr-2">✓</span>
                <span className="text-gray-700 dark:text-gray-300">Advanced filtering & search</span>
              </li>
              <li className="flex items-start">
                <span className="text-green-500 mr-2">✓</span>
                <span className="text-gray-700 dark:text-gray-300">Activity timeline</span>
              </li>
              <li className="flex items-start">
                <span className="text-green-500 mr-2">✓</span>
                <span className="text-gray-700 dark:text-gray-300">Multiple view modes</span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}
