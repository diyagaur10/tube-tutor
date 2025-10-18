import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { videoService } from '../services/auth'
import { Play, Clock, User } from 'lucide-react'

const Home = () => {
  const [videos, setVideos] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadVideos()
  }, [])

  const loadVideos = async () => {
    try {
      const data = await videoService.getVideos()
      setVideos(data)
    } catch (error) {
      console.error('Failed to load videos:', error)
    } finally {
      setLoading(false)
    }
  }

  const formatDuration = (seconds) => {
    if (!seconds) return '--:--'
    const minutes = Math.floor(seconds / 60)
    const remainingSeconds = Math.floor(seconds % 60)
    return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="max-w-3xl mx-auto text-center mb-12">
        <h1 className="text-4xl md:text-5xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-primary-600 to-primary-500 mb-4">
          Welcome to TubeTutor
        </h1>
        <p className="text-lg text-gray-600 leading-relaxed">
          Learn through interactive videos with AI-generated questions at key moments.
        </p>
      </div>

      {videos.length === 0 ? (
        <div className="max-w-md mx-auto text-center py-16 px-4 bg-white rounded-2xl shadow-soft">
          <div className="bg-primary-50 w-20 h-20 mx-auto rounded-xl flex items-center justify-center mb-6">
            <Play className="w-10 h-10 text-primary-500" />
          </div>
          <h3 className="text-xl font-semibold text-gray-900 mb-3">No videos available</h3>
          <p className="text-gray-600">Check back later for new learning content.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {videos.map((video) => (
            <div key={video.id} className="group bg-white rounded-2xl shadow-soft overflow-hidden hover:shadow-lg transition-all duration-300 transform hover:-translate-y-1">
              <div className="aspect-video bg-primary-50 relative overflow-hidden">
                {video.thumbnail_url ? (
                  <img
                    src={video.thumbnail_url}
                    alt={video.title}
                    className="w-full h-full object-cover transform group-hover:scale-105 transition-transform duration-300"
                  />
                ) : (
                  <div className="w-full h-full flex items-center justify-center bg-gradient-to-br from-primary-100 to-primary-50">
                    <Play className="w-16 h-16 text-primary-400 opacity-50" />
                  </div>
                )}
                <div className="absolute bottom-3 right-3 bg-black/70 backdrop-blur-sm text-white text-sm px-3 py-1 rounded-full font-medium">
                  {formatDuration(video.duration)}
                </div>
              </div>
              
              <div className="p-6">
                <h3 className="font-semibold text-gray-900 text-lg mb-2 line-clamp-2 group-hover:text-primary-600 transition-colors">
                  {video.title}
                </h3>
                <p className="text-gray-600 text-sm mb-4 line-clamp-2">
                  {video.description || 'No description available'}
                </p>
                
                <div className="flex items-center justify-between text-sm text-gray-500 mb-4">
                  <div className="flex items-center space-x-2 bg-gray-50 px-3 py-1 rounded-full">
                    <User className="w-4 h-4 text-primary-500" />
                    <span className="font-medium">{video.uploader?.username || 'Unknown'}</span>
                  </div>
                  <div className="flex items-center space-x-2 bg-gray-50 px-3 py-1 rounded-full">
                    <Clock className="w-4 h-4 text-primary-500" />
                    <span className="font-medium">{formatDuration(video.duration)}</span>
                  </div>
                </div>
                
                <Link
                  to={`/video/${video.id}`}
                  className="w-full bg-gradient-to-r from-primary-600 to-primary-500 hover:from-primary-500 hover:to-primary-400 text-white font-medium py-3 px-4 rounded-xl transition-all duration-200 flex items-center justify-center space-x-2 transform hover:-translate-y-0.5"
                >
                  <span>Start Learning</span>
                  <Play className="w-4 h-4" />
                </Link>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default Home
