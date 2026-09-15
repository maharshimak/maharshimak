param(
    [string]$Owner = "maharshimak",
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"

$Projects = @(
    @{ Name = "makma-ai-os"; Description = "Tool-using personal AI runtime with persistent memory, provider routing, permissioned tools and auditable planning."; Topics = @("artificial-intelligence","ai-agents","llm","fastapi","python","ollama") },
    @{ Name = "agentic-rag-engine"; Description = "Production-minded agentic RAG engine with hybrid retrieval, reranking, citations and evaluation."; Topics = @("rag","llm","ai-agents","retrieval","python","nlp") },
    @{ Name = "multimodal-ai-studio"; Description = "Multimodal AI studio for intelligent image and video workflow planning and editing systems."; Topics = @("multimodal-ai","computer-vision","video","image-processing","generative-ai","python") },
    @{ Name = "knowledge-twin"; Description = "Knowledge intelligence system combining graph modeling, retrieval and semantic reasoning."; Topics = @("knowledge-graph","nlp","retrieval","semantic-search","python","ai") },
    @{ Name = "clinical-document-intelligence"; Description = "Synthetic-data clinical document intelligence pipeline for extraction, normalization and validation."; Topics = @("document-ai","nlp","information-extraction","healthcare-ai","python","machine-learning") },
    @{ Name = "secure-data-copilot"; Description = "Read-only analytics copilot with SQL policy enforcement, schema introspection, auditing and FastAPI."; Topics = @("data-agent","sql","fastapi","analytics","ai-agents","python") },
    @{ Name = "llm-eval-observability"; Description = "LLM evaluation and observability toolkit for relevance, citations, latency, cost and regression gates."; Topics = @("llm","llm-evaluation","observability","llmops","testing","python") },
    @{ Name = "mlops-control-plane"; Description = "MLOps control plane for model registry, dataset fingerprints, promotion gates and drift detection."; Topics = @("mlops","machine-learning","model-registry","drift-detection","python","governance") },
    @{ Name = "mlops-production-pipeline"; Description = "Inspectable ML lifecycle with training, evaluation gates, metadata and population-stability monitoring."; Topics = @("mlops","machine-learning","ci-cd","monitoring","python","testing") }
)

function Invoke-Step {
    param([string]$Command)
    Write-Host "`n> $Command" -ForegroundColor Cyan
    if (-not $DryRun) {
        Invoke-Expression $Command
        if ($LASTEXITCODE -ne 0) { throw "Command failed with exit code $LASTEXITCODE: $Command" }
    }
}

foreach ($cmd in @("git", "gh")) {
    if (-not (Get-Command $cmd -ErrorAction SilentlyContinue)) {
        throw "Required command '$cmd' is not installed or not on PATH."
    }
}

Invoke-Step "gh auth status"

$insideRepo = git rev-parse --is-inside-work-tree 2>$null
if ($insideRepo -ne "true") { throw "Run this script from a clone of maharshimak/maharshimak." }

$origin = git remote get-url origin
if ($origin -notmatch "maharshimak/maharshimak") {
    Write-Warning "Origin is '$origin'. Expected maharshimak/maharshimak. Continuing because -Owner may be intentional."
}

if ((git status --porcelain) -and -not $DryRun) {
    throw "Working tree is not clean. Commit/stash local changes before splitting repositories."
}

foreach ($project in $Projects) {
    $name = $project.Name
    $prefix = "portfolio-projects/$name"
    $repo = "$Owner/$name"
    $splitBranch = "split/$name"

    Write-Host "`n============================================================" -ForegroundColor DarkGray
    Write-Host "Migrating $name" -ForegroundColor Green
    Write-Host "============================================================" -ForegroundColor DarkGray

    if (-not (Test-Path $prefix)) {
        throw "Project directory not found: $prefix"
    }

    # Create the standalone repository only when it does not already exist.
    & gh repo view $repo --json name *> $null
    $repoExists = ($LASTEXITCODE -eq 0)

    if (-not $repoExists) {
        $descEscaped = $project.Description.Replace('"','\"')
        Invoke-Step "gh repo create $repo --public --description `"$descEscaped`""
    } else {
        Write-Host "Repository already exists: $repo" -ForegroundColor Yellow
    }

    # Preserve only the commit history that touched this project directory.
    Invoke-Step "git branch -D $splitBranch 2>`$null"
    Invoke-Step "git subtree split --prefix=`"$prefix`" -b `"$splitBranch`""

    # Push the split history as the standalone repository's main branch.
    Invoke-Step "git push --force `"https://github.com/$repo.git`" `"$splitBranch`:main"

    # Add recruiter-friendly metadata.
    $topicArgs = ($project.Topics | ForEach-Object { "--add-topic `"$_`"" }) -join " "
    Invoke-Step "gh repo edit $repo --homepage `"https://maharshipatel-portfolio.vercel.app/`" $topicArgs"

    if (-not $DryRun) {
        git branch -D $splitBranch | Out-Null
    }
}

Write-Host "`nAll standalone repositories have been created and populated." -ForegroundColor Green
Write-Host "The source folders were intentionally NOT deleted from maharshimak/maharshimak." -ForegroundColor Yellow
Write-Host "Next: validate CI/README in each repo, then update the profile README and remove migrated folders in a separate PR." -ForegroundColor Yellow
