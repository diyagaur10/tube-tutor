import React, { useState, useEffect } from 'react'
import { useAuth } from '../hooks/useAuth'
import { videoService } from '../services/auth'
import { Upload, Plus, X, Edit, Trash2 } from 'lucide-react'
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
  const [videos, setVideos] = useState([])
  const [editingVideo, setEditingVideo] = useState(null)

  useEffect(() => {
    loadVideos()
  }, [])

  const loadVideos = async () => {
    try {
      const data = await videoService.getVideos()
      setVideos(data)
    } catch (error) {
      toast.error('Failed to load videos')
      console.error(error)
    }
  }

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

  const handleEditClick = (video) => {
    setEditingVideo(video)
    setUploadData({
      title: video.title,
      description: video.description || '',
      questionTimestamps: [],
    })
    setShowUploadForm(true)
  }

  const handleDeleteVideo = async (videoId) => {
    if (window.confirm('Are you sure you want to delete this video?')) {
      try {
        await videoService.deleteVideo(videoId)
        toast.success('Video deleted successfully')
        loadVideos()
      } catch (error) {
        toast.error('Failed to delete video')
        console.error(error)
      }
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!editingVideo && !uploadData.videoFile) {
      toast.error('Please select a video file')
      return
    }

    setUploading(true)

    try {
      const formData = new FormData()
      formData.append('title', uploadData.title)
      formData.append('description', uploadData.description)
      
      if (uploadData.videoFile) {
        formData.append('video_file', uploadData.videoFile)
      }
      
      if (uploadData.questionTimestamps.length > 0) {
        formData.append('question_timestamps', JSON.stringify(uploadData.questionTimestamps))
      }

      if (editingVideo) {
        await videoService.updateVideo(editingVideo.id, formData)
        toast.success('Video updated successfully!')
      } else {
        await videoService.uploadVideo(formData)
        toast.success('Video uploaded successfully!')
      }

      setShowUploadForm(false)
      setEditingVideo(null)
      setUploadData({
        title: '',
        description: '',
        questionTimestamps: [],
      })
      loadVideos()
    } catch (error) {
      toast.error(editingVideo ? 'Failed to update video' : 'Failed to upload video')
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
          <h2 className="text-xl font-semibold text-gray-900">
            {editingVideo ? 'Edit Video' : 'Video Management'}
          </h2>
          {!editingVideo && (
            <button
              onClick={() => setShowUploadForm(!showUploadForm)}
              className="btn-primary flex items-center space-x-2"
            >
              <Plus className="w-4 h-4" />
              <span>Upload Video</span>
            </button>
          )}
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

            {!editingVideo && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Video File
                </label>
                <input
                  type="file"
                  accept="video/*"
                  required={!editingVideo}
                  onChange={handleFileChange}
                  className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-primary-50 file:text-primary-700 hover:file:bg-primary-100"
                />
              </div>
            )}

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
                {uploading 
                  ? (editingVideo ? 'Updating...' : 'Uploading...') 
                  : (editingVideo ? 'Update Video' : 'Upload Video')}
              </button>
              <button
                type="button"
                onClick={() => {
                  setShowUploadForm(false)
                  setEditingVideo(null)
                  setUploadData({
                    title: '',
                    description: '',
                    questionTimestamps: [],
                  })
                }}
                className="btn-secondary"
              >
                Cancel
              </button>
            </div>
          </form>
        )}

        {/* Video List */}
        <div className="mt-8">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Uploaded Videos</h3>
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {videos.map((video) => (
              <div key={video.id} className="bg-white rounded-lg shadow p-4 border">
                <h4 className="font-semibold text-gray-900 mb-2">{video.title}</h4>
                <p className="text-gray-600 text-sm mb-4 line-clamp-2">{video.description}</p>
                <div className="flex space-x-2">
                  <button
                    onClick={() => handleEditClick(video)}
                    className="btn-secondary text-sm py-1 px-3 flex items-center"
                  >
                    <Edit className="w-4 h-4 mr-1" />
                    Edit
                  </button>
                  <button
                    onClick={() => handleDeleteVideo(video.id)}
                    className="btn-danger text-sm py-1 px-3 flex items-center"
                  >
                    <Trash2 className="w-4 h-4 mr-1" />
                    Delete
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

export default AdminDashboard