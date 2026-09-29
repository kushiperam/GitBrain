import { useEffect, useState } from "react";
import "./App.css";

const API_BASE_URL = "http://127.0.0.1:8000";

function App() {
  // ==========================================
  // Authentication
  // ==========================================

  const [token, setToken] = useState(
    () => localStorage.getItem("gitbrain_token") || ""
  );

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const [loginLoading, setLoginLoading] = useState(false);

  // ==========================================
  // Repositories
  // ==========================================

  const [repositories, setRepositories] = useState([]);

  const [repositoryId, setRepositoryId] = useState(4);

  // ==========================================
  // Local Repository
  // ==========================================

  const [localRepositoryName, setLocalRepositoryName] =
    useState("");

  const [localRepositoryPath, setLocalRepositoryPath] =
    useState("");

  const [localRepositoryLoading, setLocalRepositoryLoading] =
    useState(false);

  // ==========================================
  // Q&A
  // ==========================================

  const [question, setQuestion] = useState(
    "How is synthetic data generated?"
  );

  const [answer, setAnswer] = useState("");

  const [sources, setSources] = useState([]);

  const [loading, setLoading] = useState(false);

  const [error, setError] = useState("");

  // ==========================================
  // Load repositories
  // ==========================================

  useEffect(() => {
    if (!token) {
      return;
    }

    const loadRepositories = async () => {
      try {
        setError("");

        const response = await fetch(
          `${API_BASE_URL}/repositories/`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        if (response.status === 401) {
          localStorage.removeItem("gitbrain_token");
          setToken("");

          setError(
            "Your session has expired. Please log in again."
          );

          return;
        }

        if (!response.ok) {
          throw new Error(
            `Failed to load repositories (${response.status})`
          );
        }

        const data = await response.json();

        // Remove duplicate repositories using their URL.
        const uniqueRepositories = Array.from(
          new Map(
            data.map((repository) => [
              repository.url,
              repository,
            ])
          ).values()
        );

        setRepositories(uniqueRepositories);

        // Keep PrivacySynthAI (ID 4) as the initial
        // repository when it exists.
        const defaultRepository = uniqueRepositories.find(
          (repository) => repository.id === 4
        );

        if (defaultRepository) {
          setRepositoryId(defaultRepository.id);
        } else if (uniqueRepositories.length > 0) {
          setRepositoryId(uniqueRepositories[0].id);
        }
      } catch (err) {
        console.error(
          "Repository loading error:",
          err
        );

        setError(
          err.message ||
            "Unable to load repositories from GitBrain."
        );
      }
    };

    loadRepositories();
  }, [token]);

  // ==========================================
  // Login
  // ==========================================

  const login = async (event) => {
    event.preventDefault();

    if (!username.trim() || !password) {
      setError(
        "Please enter your username and password."
      );

      return;
    }

    setLoginLoading(true);
    setError("");

    try {
      const formData = new URLSearchParams();

      formData.append(
        "username",
        username.trim()
      );

      formData.append(
        "password",
        password
      );

      const response = await fetch(
        `${API_BASE_URL}/auth/login`,
        {
          method: "POST",

          headers: {
            "Content-Type":
              "application/x-www-form-urlencoded",
          },

          body: formData.toString(),
        }
      );

      const data = await response
        .json()
        .catch(() => null);

      if (!response.ok) {
        throw new Error(
          data?.detail ||
            `Login failed with status ${response.status}`
        );
      }

      localStorage.setItem(
        "gitbrain_token",
        data.access_token
      );

      setToken(data.access_token);

      setPassword("");
    } catch (err) {
      console.error(
        "Login error:",
        err
      );

      setError(
        err.message ||
          "Unable to log in to GitBrain."
      );
    } finally {
      setLoginLoading(false);
    }
  };

  // ==========================================
  // Logout
  // ==========================================

  const logout = () => {
    localStorage.removeItem(
      "gitbrain_token"
    );

    setToken("");

    setRepositories([]);

    setAnswer("");

    setSources([]);

    setError("");
  };

  // ==========================================
  // Add Local Repository
  // ==========================================

  const addLocalRepository = async () => {
    if (!localRepositoryName.trim()) {
      setError(
        "Please enter a name for the local repository."
      );

      return;
    }

    if (!localRepositoryPath.trim()) {
      setError(
        "Please enter the full local folder path."
      );

      return;
    }

    setLocalRepositoryLoading(true);
    setError("");

    try {
      const response = await fetch(
        `${API_BASE_URL}/repositories/local`,
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },

          body: JSON.stringify({
            name: localRepositoryName.trim(),

            url: `local://${Date.now()}`,

            source_type: "local",

            local_path:
              localRepositoryPath.trim(),
          }),
        }
      );

      if (response.status === 401) {
        logout();

        setError(
          "Your session has expired. Please log in again."
        );

        return;
      }

      const data = await response
        .json()
        .catch(() => null);

      if (!response.ok) {
        throw new Error(
          data?.detail ||
            `Failed to add local repository (${response.status})`
        );
      }

      // Add the new repository to the dropdown.
      setRepositories(
        (currentRepositories) => [
          ...currentRepositories,
          data,
        ]
      );

      // Automatically select the newly added repository.
      setRepositoryId(data.id);

      // Clear the local repository form.
      setLocalRepositoryName("");

      setLocalRepositoryPath("");

      setAnswer("");

      // IMPORTANT:
      // Sources must remain an array.
      setSources([]);

      setError("");
    } catch (err) {
      console.error(
        "Local repository error:",
        err
      );

      setError(
        err.message ||
          "Unable to add the local repository."
      );
    } finally {
      setLocalRepositoryLoading(false);
    }
  };

  // ==========================================
  // Ask GitBrain
  // ==========================================

  const askGitBrain = async () => {
    if (!question.trim()) {
      setError(
        "Please enter a question."
      );

      return;
    }

    if (!repositoryId) {
      setError(
        "Please select a repository."
      );

      return;
    }

    setLoading(true);

    setError("");

    setAnswer("");

    setSources([]);

    try {
      const response = await fetch(
        `${API_BASE_URL}/repositories/${repositoryId}/ask`,
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },

          body: JSON.stringify({
            question:
              question.trim(),
          }),
        }
      );

      if (response.status === 401) {
        logout();

        setError(
          "Your session has expired. Please log in again."
        );

        return;
      }

      if (!response.ok) {
        const errorData = await response
          .json()
          .catch(() => null);

        throw new Error(
          errorData?.detail ||
            `Request failed with status ${response.status}`
        );
      }

      const data = await response.json();

      setAnswer(
        data.answer || ""
      );

      setSources(
        data.sources || []
      );
    } catch (err) {
      console.error(
        "GitBrain error:",
        err
      );

      setError(
        err.message ||
          "Unable to connect to the GitBrain backend."
      );
    } finally {
      setLoading(false);
    }
  };

  // ==========================================
  // Login Screen
  // ==========================================

  if (!token) {
    return (
      <div className="app">
        <div className="container">

          <header className="header">

            <div className="logo">
              GitBrain
            </div>

            <h1>
              Repository Memory Engine
            </h1>

            <p>
              Sign in to access your repositories.
            </p>

          </header>

          <form
            className="section"
            onSubmit={login}
          >

            <label htmlFor="username">
              Username
            </label>

            <input
              id="username"
              type="text"
              value={username}
              onChange={(event) =>
                setUsername(
                  event.target.value
                )
              }
              placeholder="Enter your username"
              disabled={loginLoading}
            />

            <label htmlFor="password">
              Password
            </label>

            <input
              id="password"
              type="password"
              value={password}
              onChange={(event) =>
                setPassword(
                  event.target.value
                )
              }
              placeholder="Enter your password"
              disabled={loginLoading}
            />

            <button
              className="ask-button"
              type="submit"
              disabled={loginLoading}
            >
              {loginLoading
                ? "Signing in..."
                : "Login"}
            </button>

          </form>

          {error && (
            <div className="error">
              <strong>
                Error:
              </strong>{" "}
              {error}
            </div>
          )}

          <footer className="footer">
            GitBrain • Repository Memory Engine
          </footer>

        </div>
      </div>
    );
  }

  // ==========================================
  // Main GitBrain Screen
  // ==========================================

  return (
    <div className="app">

      <div className="container">

        {/* Header */}

        <header className="header">

          <div className="logo">
            GitBrain
          </div>

          <h1>
            Repository Memory Engine
          </h1>

          <p>
            Ask questions about your software
            repository using AI-powered code search.
          </p>

          <button
            type="button"
            onClick={logout}
          >
            Logout
          </button>

        </header>


        {/* Repository Selection */}

        <section className="section">

          <label htmlFor="repository">
            Repository
          </label>

          <select
            id="repository"
            value={repositoryId}
            onChange={(event) =>
              setRepositoryId(
                Number(
                  event.target.value
                )
              )
            }
            disabled={
              loading ||
              repositories.length === 0
            }
          >

            {repositories.map(
              (repository) => (
                <option
                  key={repository.url}
                  value={repository.id}
                >
                  {repository.source_type ===
                  "local"
                    ? `📁 ${repository.name}`
                    : repository.name}
                </option>
              )
            )}

          </select>

        </section>


        {/* Add Local Repository */}

        <section className="section">

          <h2>
            Add Local Folder
          </h2>

          <p>
            Add a folder from this computer by
            entering its full Windows path.
          </p>

          <label htmlFor="localRepositoryName">
            Project Name
          </label>

          <input
            id="localRepositoryName"
            type="text"
            value={localRepositoryName}
            onChange={(event) =>
              setLocalRepositoryName(
                event.target.value
              )
            }
            placeholder="Example: My Python Project"
            disabled={
              localRepositoryLoading
            }
          />

          <label htmlFor="localRepositoryPath">
            Folder Path
          </label>

          <input
            id="localRepositoryPath"
            type="text"
            value={localRepositoryPath}
            onChange={(event) =>
              setLocalRepositoryPath(
                event.target.value
              )
            }
            placeholder={
              "C:\\Users\\YourName\\Documents\\MyProject"
            }
            disabled={
              localRepositoryLoading
            }
          />

          <button
            className="ask-button"
            type="button"
            onClick={
              addLocalRepository
            }
            disabled={
              localRepositoryLoading
            }
          >
            {localRepositoryLoading
              ? "Adding Local Folder..."
              : "Add Local Folder"}
          </button>

        </section>


        {/* Question */}

        <section className="section">

          <label htmlFor="question">
            Ask your repository
          </label>

          <textarea
            id="question"
            value={question}
            onChange={(event) =>
              setQuestion(
                event.target.value
              )
            }
            placeholder="Ask a question about your repository..."
            rows="4"
            disabled={loading}
          />

        </section>


        {/* Ask Button */}

        <button
          className="ask-button"
          onClick={askGitBrain}
          disabled={
            loading ||
            repositories.length === 0
          }
        >
          {loading
            ? "GitBrain is thinking..."
            : "Ask GitBrain"}
        </button>


        {/* Error */}

        {error && (
          <div className="error">

            <strong>
              Error:
            </strong>{" "}

            {error}

          </div>
        )}


        {/* Answer */}

        {answer && !error && (
          <section className="result">

            <h2>
              AI Answer
            </h2>

            <div className="answer">
              {answer}
            </div>

          </section>
        )}


        {/* Sources */}

        {sources.length > 0 &&
          !error && (
            <section className="result">

              <h2>
                Sources
              </h2>

              <p className="source-description">
                Repository code used to generate
                this answer.
              </p>

              {sources.map(
                (source, index) => (
                  <div
                    className="source"
                    key={index}
                  >

                    <div className="source-file">
                      📄 {source.file}
                    </div>

                    <div className="source-detail">
                      Lines{" "}
                      {source.start_line}{" "}
                      -{" "}
                      {source.end_line}
                    </div>

                    <div className="source-detail">
                      Similarity:{" "}
                      {source.score.toFixed(
                        4
                      )}
                    </div>

                  </div>
                )
              )}

            </section>
          )}


        {/* Footer */}

        <footer className="footer">
          GitBrain • Repository Memory Engine
        </footer>

      </div>

    </div>
  );
}

export default App;