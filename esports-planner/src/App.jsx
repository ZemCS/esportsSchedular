import React, { useState } from "react";

const App = () => {
  const [vlrTeams, setVlrTeams] = useState([]);
  const [lolTeams, setLolTeams] = useState([]);

  const vlrTeamOptions = ["FNATIC", "Sentinels", "G2", "Team Vitality"];
  const lolTeamOptions = ["FNC", "G2", "T1", "GEN", "DK", "HLE", "LR"];

  const handleCheckBoxChange = (team, type) => {
    if (type === "vlr") {
      setVlrTeams((prev) =>
        prev.includes(team) ? prev.filter((t) => t !== team) : [...prev, team]
      );
    } else if (type === "lol") {
      setLolTeams((prev) =>
        prev.includes(team) ? prev.filter((t) => t !== team) : [...prev, team]
      );
    }
  };

  const submitTeams = () => {
    const payload = {
      vlrTeams,
      lolTeams,
    };

    fetch("http://127.0.0.1:5000/update-teams", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    })
      .then((response) => response.json())
      .then((data) => alert(data.message))
      .catch((error) => console.error("Error: ", error));
  };

  return (
    <div className="h-screen bg-white flex items-center justify-center">
      <div className="w-full max-w-2xl bg-white rounded-lg shadow-lg p-8">
        <h1 className="text-3xl font-bold text-center mb-8 text-gray-800">
          Select Your Favorite Teams
        </h1>

        {/* Valorant Teams Section */}
        <div className="mb-8">
          <h2 className="text-xl font-semibold text-gray-700 mb-4">Valorant Teams</h2>
          <div className="grid grid-cols-2 gap-4">
            {vlrTeamOptions.map((team) => (
              <label
                key={team}
                className="flex items-center space-x-3 bg-gray-50 p-3 rounded-lg border hover:border-blue-400 transition"
              >
                <input
                  type="checkbox"
                  value={team}
                  onChange={() => handleCheckBoxChange(team, "vlr")}
                  className="form-checkbox h-5 w-5 text-blue-500"
                />
                <span className="text-gray-800">{team}</span>
              </label>
            ))}
          </div>
        </div>

        {/* League Teams Section */}
        <div className="mb-8">
          <h2 className="text-xl font-semibold text-gray-700 mb-4">League Teams</h2>
          <div className="grid grid-cols-2 gap-4">
            {lolTeamOptions.map((team) => (
              <label
                key={team}
                className="flex items-center space-x-3 bg-gray-50 p-3 rounded-lg border hover:border-blue-400 transition"
              >
                <input
                  type="checkbox"
                  value={team}
                  onChange={() => handleCheckBoxChange(team, "lol")}
                  className="form-checkbox h-5 w-5 text-blue-500"
                />
                <span className="text-gray-800">{team}</span>
              </label>
            ))}
          </div>
        </div>

        {/* Submit Button */}
        <button
          className="w-full bg-blue-500 text-white py-3 rounded-lg font-semibold hover:bg-blue-600 transition"
          onClick={submitTeams}
        >
          Submit Teams
        </button>
      </div>
    </div>
  );
};

export default App;
