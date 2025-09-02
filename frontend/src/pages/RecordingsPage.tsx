import React, { useEffect, useState } from "react";
import { parseFilePath } from "../utils";
import { useAuth } from "../contexts/AuthContext";

interface Recording {
  id: number;
  s3_filepath: string;
  rec_date: string;
  school: string;
  timestamp: string;
  cam_id: string;
  camera_name: string;
}

const RecordingsPage = () => {
  const [recordings, setRecordings] = useState<Recording[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { user } = useAuth();

  useEffect(() => {
    if (!user) return;

    const fetchRecordings = async () => {
      try {
        const token = await user.getIdToken();
        const response = await fetch("http://127.0.0.1:8000/api/recordings/", {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        setRecordings(data);
      } catch (err) {
        console.error("Error fetching recordings:", err);
        setError(err instanceof Error ? err.message : "Failed to fetch recordings");
      } finally {
        setLoading(false);
      }
    };

    fetchRecordings();
  }, [user]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <span className="text-gray-500">Loading…</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <p className="text-red-500 mb-2">Error loading recordings</p>
          <p className="text-gray-600 text-sm">{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <h2 className="text-3xl font-bold text-center mb-6">
        Recordings
      </h2>

      <div className="overflow-x-auto bg-white shadow-lg rounded-lg">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wide">
                School Name
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wide">
                Start Time
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wide">
                End Time
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wide">
                Cam Name
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wide">
                Cam ID
              </th>
            </tr>
          </thead>

          <tbody className="bg-white divide-y divide-gray-100">
            {recordings.map((rec) => (
              <tr
                key={rec.id}
                className="hover:bg-gray-50 transition-colors"
                onClick={async () => {
                  try {
                    const token = await user?.getIdToken();
                    const response = await fetch(
                      `http://127.0.0.1:8000/api/recordings/${rec.id}/download/`,
                      {
                        headers: {
                          'Authorization': `Bearer ${token}`,
                        },
                      }
                    );
                    
                    if (response.ok) {
                      const blob = await response.blob();
                      const url = window.URL.createObjectURL(blob);
                      const a = document.createElement('a');
                      a.href = url;
                      a.download = parseFilePath(rec.s3_filepath);
                      document.body.appendChild(a);
                      a.click();
                      window.URL.revokeObjectURL(url);
                      document.body.removeChild(a);
                    }
                  } catch (err) {
                    console.error("Download error:", err);
                  }
                }}
                style={{ cursor: "pointer" }}
              >
                <td className="px-6 py-4 whitespace-nowrap">
                  {parseFilePath(rec.s3_filepath)}
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  {new Date(rec.timestamp).toLocaleString()}
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  {new Date(rec.rec_date).toLocaleString()}
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  {rec.camera_name || "—"}
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  {rec.cam_id || "—"}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default RecordingsPage;