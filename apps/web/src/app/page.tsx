"use client"
import { useState, useEffect } from 'react'
import { ScoreDistributionChart } from '../components/AnalyticsCharts'
import { Briefcase, UploadCloud, Users, Sparkles, CheckCircle, AlertTriangle } from 'lucide-react'

export default function Dashboard() {
  const [jobId, setJobId] = useState<string | null>(null)
  const [jobs, setJobs] = useState<any[]>([])
  const [candidates, setCandidates] = useState<any[]>([])
  const [loading, setLoading] = useState(false)

  const API_BASE = "http://localhost:8000/api"

  useEffect(() => {
    fetchJobs()
  }, [])

  async function fetchJobs() {
    try {
      const res = await fetch(`${API_BASE}/jobs`)
      if (res.ok) {
        const data = await res.json()
        setJobs(data)
        if (data.length > 0 && !jobId) setJobId(data[0].id)
      }
    } catch (e) {
      console.error("Failed to fetch jobs")
    }
  }

  async function createDemoJob() {
    setLoading(true)
    const payloads = [
      {
        title: "Data Analyst",
        jd_text: "We are looking for a Data Analyst with 2+ years of experience. Must be proficient in SQL, Python, and Excel. Experience with Power BI or Tableau is a plus.",
        must_have: ["sql", "python", "excel"],
        nice_to_have: ["power bi", "tableau"],
        min_exp_years: 2.0
      },
      {
        title: "Backend Python Developer",
        jd_text: "Seeking a Python Developer with 3+ years of experience. Must have strong skills in Python and Django. Experience with Docker and SQL is required.",
        must_have: ["python", "django", "docker", "sql"],
        nice_to_have: ["react", "gcp"],
        min_exp_years: 3.0
      },
      {
        title: "Frontend React Developer",
        jd_text: "Looking for a Frontend Developer proficient in React, JavaScript, HTML, and CSS. Next.js experience is a huge plus.",
        must_have: ["react", "javascript", "html", "css"],
        nice_to_have: ["next.js", "git"],
        min_exp_years: 1.0
      },
      {
        title: "DevOps Engineer",
        jd_text: "We need a DevOps Engineer with AWS and Kubernetes experience. Must know Linux and Docker.",
        must_have: ["aws", "kubernetes", "linux", "docker"],
        nice_to_have: ["python", "git"],
        min_exp_years: 4.0
      }
    ];
    
    try {
      for (const payload of payloads) {
        await fetch(`${API_BASE}/jobs`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
      }
      fetchJobs();
    } catch (e) {
      console.error(e)
    }
    setLoading(false)
  }

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files || e.target.files.length === 0) return;
    setLoading(true);
    
    for (let i = 0; i < e.target.files.length; i++) {
      const file = e.target.files[i];
      const formData = new FormData();
      formData.append("file", file);
      // Format name from filename (e.g. "resume1.txt" -> "Resume1")
      const formattedName = file.name.split('.')[0].charAt(0).toUpperCase() + file.name.split('.')[0].slice(1);
      formData.append("candidate_name", formattedName);

      try {
        await fetch(`${API_BASE}/resumes/upload`, {
          method: 'POST',
          body: formData
        });
      } catch (err) {
        console.error("Failed to upload", file.name);
      }
    }
    
    setLoading(false);
    alert("Resumes uploaded successfully! Click 'Analyze Candidates' to view results.");
    e.target.value = '';
  }

  async function runRanking() {
    if (!jobId) return
    setLoading(true)
    try {
      // 1. Rank
      await fetch(`${API_BASE}/rank/${jobId}`, { method: 'POST' })
      // 2. Fetch results
      const res = await fetch(`${API_BASE}/rankings/${jobId}`)
      if (res.ok) {
        setCandidates(await res.json())
      }
    } catch (e) {
      console.error(e)
    }
    setLoading(false)
  }

  return (
    <div className="min-h-screen p-8 text-white max-w-7xl mx-auto flex flex-col gap-8">
      
      {/* Header */}
      <header className="flex items-center justify-between glass-panel rounded-2xl p-6">
        <div className="flex items-center gap-4">
          <div className="bg-gradient-to-br from-indigo-500 to-purple-600 p-3 rounded-xl">
            <Sparkles className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-2xl font-bold tracking-tight">AI Resume Screening</h1>
            <p className="text-white/60 text-sm">Automated shortlisting & candidate analysis</p>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <button onClick={createDemoJob} className="px-4 py-2 bg-white/10 hover:bg-white/20 transition-colors rounded-lg flex items-center gap-2 text-sm font-medium">
            <Briefcase className="w-4 h-4" /> Create Demo Job
          </button>
          <label className="px-4 py-2 bg-white/10 hover:bg-white/20 transition-colors rounded-lg flex items-center gap-2 text-sm font-medium cursor-pointer">
            <UploadCloud className="w-4 h-4" /> Upload Resumes
            <input type="file" multiple accept=".txt,.pdf,.docx" className="hidden" onChange={handleFileUpload} disabled={loading} />
          </label>
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Left Column: Controls & Analytics */}
        <div className="lg:col-span-1 space-y-8">
          
          <div className="glass-panel rounded-2xl p-6">
            <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
              <Briefcase className="w-5 h-5 text-indigo-400" /> Active Job Role
            </h2>
            <select 
              className="w-full bg-black/20 border border-white/10 rounded-lg p-3 text-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
              value={jobId || ""}
              onChange={(e) => setJobId(e.target.value)}
            >
              <option value="" disabled>Select a job...</option>
              {jobs.map(j => (
                <option key={j.id} value={j.id}>{j.title} (ID: {j.id.substring(0,8)})</option>
              ))}
            </select>
            
            <button 
              onClick={runRanking}
              disabled={!jobId || loading}
              className="w-full mt-6 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 disabled:opacity-50 transition-all rounded-lg py-3 font-medium shadow-lg flex items-center justify-center gap-2"
            >
              {loading ? <span className="animate-pulse">Processing...</span> : <><Users className="w-5 h-5" /> Analyze Candidates</>}
            </button>
          </div>

          {candidates.length > 0 && (
            <ScoreDistributionChart data={candidates} />
          )}

        </div>

        {/* Right Column: Ranked Candidates */}
        <div className="lg:col-span-2 glass-panel rounded-2xl p-6">
          <h2 className="text-xl font-semibold mb-6 flex items-center gap-2">
            <Users className="w-5 h-5 text-purple-400" /> Ranked Candidates
          </h2>
          
          {candidates.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-64 text-white/40">
              <Users className="w-12 h-12 mb-4 opacity-50" />
              <p>No candidates analyzed yet.</p>
              <p className="text-sm">Select a job and click Analyze Candidates.</p>
            </div>
          ) : (
            <div className="space-y-4">
              {candidates.map((c, i) => (
                <div key={i} className="bg-white/5 border border-white/10 rounded-xl p-5 hover:bg-white/10 transition-colors">
                  <div className="flex justify-between items-start mb-4">
                    <div>
                      <h3 className="text-lg font-bold flex items-center gap-2">
                        <span className="text-white/50 text-sm">#{i+1}</span> {c.name}
                      </h3>
                      <p className="text-white/60 text-sm mt-1">{c.candidate_id}</p>
                    </div>
                    <div className="text-right">
                      <div className={`text-2xl font-bold ${c.score > 0.7 ? 'text-emerald-400' : c.score > 0.5 ? 'text-amber-400' : 'text-rose-400'}`}>
                        {(c.score * 100).toFixed(1)}%
                      </div>
                      <p className="text-white/50 text-xs">Match Score</p>
                    </div>
                  </div>
                  
                  <div className="grid grid-cols-2 gap-4 text-sm bg-black/20 p-4 rounded-lg">
                    <div>
                      <span className="text-white/50 block mb-1">Top Skills Match</span>
                      <div className="flex flex-wrap gap-2">
                        {c.reasons.matched_skills_list?.map((s: string, idx: number) => (
                          <span key={idx} className="bg-indigo-500/20 text-indigo-300 px-2 py-0.5 rounded text-xs border border-indigo-500/30">
                            {s}
                          </span>
                        ))}
                      </div>
                    </div>
                    <div>
                      <span className="text-white/50 block mb-1">Analysis Flags</span>
                      <ul className="space-y-1">
                        <li className="flex items-center gap-1.5">
                          {c.reasons.experience_ok ? <CheckCircle className="w-3.5 h-3.5 text-emerald-400" /> : <AlertTriangle className="w-3.5 h-3.5 text-amber-400" />}
                          <span className={c.reasons.experience_ok ? "text-white/80" : "text-amber-300"}>Experience: {c.reasons.years_exp} yrs</span>
                        </li>
                        <li className="flex items-center gap-1.5 text-white/80">
                           <Sparkles className="w-3.5 h-3.5 text-purple-400" /> 
                           Semantic Sim: {(c.reasons.similarity * 100).toFixed(0)}%
                        </li>
                      </ul>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
