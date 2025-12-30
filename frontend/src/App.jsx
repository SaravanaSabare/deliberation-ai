import { useState } from 'react'
import './App.css'

// In production (Vercel), API is at /api
// In development, use localhost backend
const API_URL = import.meta.env.VITE_API_URL || '/api'

function App() {
  const [question, setQuestion] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const [expandedSections, setExpandedSections] = useState({
    judge: false,
    pro: false,
    con: false,
    alternative: false
  })

  const handleSubmit = async () => {
    if (!question.trim()) return

    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const response = await fetch(`${API_URL}/debate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: question.trim() })
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      setResult(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const toggleSection = (section) => {
    setExpandedSections(prev => ({
      ...prev,
      [section]: !prev[section]
    }))
  }

  return (
    <div className="app">
      <h1>Deliberation AI</h1>
      
      <div className="input-section">
        <textarea
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Enter your question..."
          rows="6"
          disabled={loading}
        />
        
        <div className="example-questions">
          <span className="example-label">Try these:</span>
          <button 
            className="example-btn" 
            onClick={() => setQuestion("Should I invest in cryptocurrency?")}
            disabled={loading}
          >
            Cryptocurrency investment
          </button>
          <button 
            className="example-btn" 
            onClick={() => setQuestion("Is remote work better than office work?")}
            disabled={loading}
          >
            Remote vs office work
          </button>
          <button 
            className="example-btn" 
            onClick={() => setQuestion("Should I learn Python or JavaScript first?")}
            disabled={loading}
          >
            Python vs JavaScript
          </button>
        </div>
        
        <button 
          onClick={handleSubmit} 
          disabled={loading || !question.trim()}
          className="submit-btn"
        >
          {loading ? 'Running Deliberation...' : 'Run Deliberation'}
        </button>
      </div>

      {error && (
        <div className="error">
          <strong>Error:</strong> {error}
        </div>
      )}

      {result && (
        <div className="results">
          <div className="final-answer">
            <div className="answer-header">
              <h2>Final Answer</h2>
              {result.confidence && (
                <span className={`confidence confidence-${result.confidence}`}>
                  {result.confidence}
                </span>
              )}
            </div>
            <p>{result.final_answer}</p>
            {result.confidence && (
              <div className="confidence-explanation">
                Confidence is derived from agreement across 3 independent deliberations.
              </div>
            )}
          </div>

          {result.what_would_change && (
            <div className="what-would-change">
              <h3>What Would Change This Answer?</h3>
              <p>{result.what_would_change}</p>
            </div>
          )}

          <div className="reasoning-label">Reasoning Details</div>

          <div className="collapsible-section">
            <button 
              className="collapsible-header"
              onClick={() => toggleSection('judge')}
            >
              <span>Judge Decision</span>
              <span>{expandedSections.judge ? '▼' : '▶'}</span>
            </button>
            {expandedSections.judge && (
              <div className="collapsible-content">
                <p>{result.judge_decision}</p>
              </div>
            )}
          </div>

          <div className="collapsible-section">
            <button 
              className="collapsible-header"
              onClick={() => toggleSection('pro')}
            >
              <span>Pro Agent</span>
              <span>{expandedSections.pro ? '▼' : '▶'}</span>
            </button>
            {expandedSections.pro && (
              <div className="collapsible-content">
                <p>{result.raw_agents?.pro || 'N/A'}</p>
              </div>
            )}
          </div>

          <div className="collapsible-section">
            <button 
              className="collapsible-header"
              onClick={() => toggleSection('con')}
            >
              <span>Con Agent</span>
              <span>{expandedSections.con ? '▼' : '▶'}</span>
            </button>
            {expandedSections.con && (
              <div className="collapsible-content">
                <p>{result.raw_agents?.con || 'N/A'}</p>
              </div>
            )}
          </div>

          <div className="collapsible-section">
            <button 
              className="collapsible-header"
              onClick={() => toggleSection('alternative')}
            >
              <span>Alternative Agent</span>
              <span>{expandedSections.alternative ? '▼' : '▶'}</span>
            </button>
            {expandedSections.alternative && (
              <div className="collapsible-content">
                <p>{result.raw_agents?.alternative || 'N/A'}</p>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}

export default App
