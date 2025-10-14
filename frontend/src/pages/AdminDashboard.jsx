import React, { useState } from 'react'
import { useAuth } from '../hooks/useAuth'
import { videoService } from '../services/auth'
import { Upload, Plus, X } from 'lucide-react'
import toast from 'react-hot-toast'

const AdminDashboard = () => {
  const { user } = useAuth()
  const [showUploadForm, setShowUploadForm] = useState(false)
  const [uploadData, setUploadData] = useState({
    title: '',
    description: '',
    questionTimestamps: [],
  })
  const [uploading, setUploading] = useState(false)

  if (!user?.is_admin) {
    return (
      <div className="text-center py-12">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">Access Denied</h2>
        <p className="text-gray-600">You need admin privileges to access this page.</p>
      </div>
    )
  }

  const handleFileChange = (e) => {
    setUploadData({
      ...uploadData,
      videoFile: e.target.files[0],
    })
  }

  const addTimestamp = () => {
    setUploadData({
      ...uploadData,
      questionTimestamps: [...uploadData.questionTimestamps, 0],
    })
  }

  const removeTimestamp = (index) => {
    setUploadData({
      ...uploadData,
      questionTimestamps: uploadData.questionTimestamps.filter((_, i) => i !== index),
    })
  }

  const updateTimestamp = (index, value) => {
    const newTimestamps = [...uploadData.questionTimestamps]
    newTimestamps[index] = parseFloat(value) || 0
    setUploadData({
      ...uploadData,
      questionTimestamps: newTimestamps,
    })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!uploadData.videoFile) {
      toast.error('Please select a video file')
      return
    }

    setUploading(true)

    try {
      const formData = new FormData()
      formData.append('title', uploadData.title)
      formData.append('description', uploadData.description)
      formData.append('question_timestamps', JSON.stringify(uploadData.questionTimestamps))
      formData.append('video_file', uploadData.videoFile)

      await videoService.uploadVideo(formData)
      toast.success('Video uploaded successfully!')
      setShowUploadForm(false)
      setUploadData({
        title: '',
        description: '',
        questionTimestamps: [],
      })
    } catch (error) {
      toast.error('Failed to upload video')
      console.error(error)
    } finally {
      setUploading(false)
    }
  }

  return (
    <div className="px-4 sm:px-6 lg:px-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Admin Dashboard</h1>
        <p className="text-gray-600">Manage videos and learning content.</p>
      </div>

      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-xl font-semibold text-gray-900">Video Management</h2>
          <button
            onClick={() => setShowUploadForm(!showUploadForm)}
            className="btn-primary flex items-center space-x-2"
          >
            <Plus className="w-4 h-4" />
            <span>Upload Video</span>
          </button>
        </div>

        {showUploadForm && (
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Video Title
              </label>
              <input
                type="text"
                required
                className="input-field"
                value={uploadData.title}
                onChange={(e) => setUploadData({ ...uploadData, title: e.target.value })}
                placeholder="Enter video title"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Description
              </label>
              <textarea
                className="input-field"
                rows={3}
                value={uploadData.description}
                onChange={(e) => setUploadData({ ...uploadData, description: e.target.value })}
                placeholder="Enter video description"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Video File
              </label>
              <input
                type="file"
                accept="video/*"
                required
                onChange={handleFileChange}
                className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-primary-50 file:text-primary-700 hover:file:bg-primary-100"
              />
            </div>

            <div>
              <div className="flex items-center justify-between mb-2">
                <label className="block text-sm font-medium text-gray-700">
                  Question Timestamps (seconds)
                </label>
                <button
                  type="button"
                  onClick={addTimestamp}
                  className="text-primary-600 hover:text-primary-700 text-sm font-medium"
                >
                  + Add Timestamp
                </button>
              </div>
              <div className="space-y-2">
                {uploadData.questionTimestamps.map((timestamp, index) => (
                  <div key={index} className="flex items-center space-x-2">
                    <input
                      type="number"
                      min="0"
                      step="1"
                      className="input-field flex-1"
                      value={timestamp}
                      onChange={(e) => updateTimestamp(index, e.target.value)}
                      placeholder="Timestamp in seconds"
                    />
                    <button
                      type="button"
                      onClick={() => removeTimestamp(index)}
                      className="text-red-600 hover:text-red-700"
                    >
                      <X className="w-4 h-4" />
                    </button>
                  </div>
                ))}
              </div>
              <p className="text-xs text-gray-500 mt-1">
                Questions will be automatically generated at these timestamps
              </p>
            </div>

            <div className="flex space-x-3">
              <button
                type="submit"
                disabled={uploading}
                className="btn-primary flex-1 disabled:opacity-50"
              >
                {uploading ? 'Uploading...' : 'Upload Video'}
              </button>
              <button
                type="button"
                onClick={() => setShowUploadForm(false)}
                className="btn-secondary"
              >
                Cancel
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  )
}

export default AdminDashboard
