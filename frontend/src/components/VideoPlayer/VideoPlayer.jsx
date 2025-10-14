import React, { useState, useEffect, useRef } from 'react'
import { useParams } from 'react-router-dom'
import { videoService, questionService, progressService } from '../services/auth'
import QuestionModal from '../components/VideoPlayer/QuestionModal'
import ProgressBar from '../components/VideoPlayer/ProgressBar'
import toast from 'react-hot-toast'

const VideoPlayer = () => {
  const { id } = useParams()
  const videoRef = useRef(null)
  const [video, setVideo] = useState(null)
  const [questions, setQuestions] = useState([])
  const [progress, setProgress] = useState({})
  const [currentTime, setCurrentTime] = useState(0)
  const [showModal, setShowModal] = useState(false)
  const [currentQuestion, setCurrentQuestion] = useState(null)
  const [isBlocked, setIsBlocked] = useState(false)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadVideoData()
  }, [id])

  useEffect(() => {
    if (video && questions.length > 0) {
      checkForQuestion()
    }
  }, [currentTime, questions, progress])

  const loadVideoData = async () => {
    try {
      const [videoData, questionsData, progressData] = await Promise.all([
        videoService.getVideo(id),
        videoService.getVideoQuestions(id),
        progressService.getProgress(id),
      ])
      
      setVideo(videoData)
      setQuestions(questionsData)
      setProgress(progressData)
      
      // Set video to last known position
      if (progressData.current_timestamp > 0) {
        setTimeout(() => {
          if (videoRef.current) {
            videoRef.current.currentTime = progressData.current_timestamp
          }
        }, 1000)
      }
    } catch (error) {
      toast.error('Failed to load video data')
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  const checkForQuestion = () => {
    const question = questions.find(q => 
      Math.abs(q.timestamp - currentTime) < 2 && 
      !progress.completed_questions?.includes(q.id)
    )
    
    if (question && !isBlocked) {
      triggerQuestion(question)
    }
  }

  const triggerQuestion = (question) => {
    setIsBlocked(true)
    setCurrentQuestion(question)
    setShowModal(true)
    if (videoRef.current) {
      videoRef.current.pause()
    }
  }

  const handleAnswerSubmit = async (answer) => {
    try {
      const response = await questionService.submitAnswer(
        currentQuestion.id, 
        answer, 
        currentTime
      )
      
      if (response.correct) {
        setShowModal(false)
        setIsBlocked(false)
        updateProgress(currentQuestion.id)
        if (videoRef.current) {
          videoRef.current.play()
        }
        toast.success('Correct answer!')
      } else {
        if (response.retries_left > 0) {
          toast.error(`Incorrect. ${response.retries_left} retries left.`)
        } else {
          // Rewind video
          const newTime = Math.max(0, currentTime - response.rewind_seconds)
          if (videoRef.current) {
            videoRef.current.currentTime = newTime
          }
          setShowModal(false)
          setIsBlocked(false)
          toast.error('Answer incorrect. Video rewound.')
        }
      }
    } catch (error) {
      toast.error('Failed to submit answer')
      console.error(error)
    }
  }

  const updateProgress = async (questionId) => {
    try {
      const completedQuestions = [...(progress.completed_questions || []), questionId]
      setProgress(prev => ({
        ...prev,
        completed_questions: completedQuestions
      }))
      
      await progressService.updateProgress(id, currentTime)
    } catch (error) {
      console.error('Failed to update progress:', error)
    }
  }

  const handleSeek = (newTime) => {
    if (isBlocked) {
      return false
    }
    
    const incompleteQuestion = questions.find(q => 
      q.timestamp <= newTime && 
      !progress.completed_questions?.includes(q.id)
    )
    
    if (incompleteQuestion) {
      toast.error('Complete previous questions first')
      return false
    }
    
    return true
  }

  const handleTimeUpdate = (e) => {
    setCurrentTime(e.target.currentTime)
  }

  const handleSeeked = (e) => {
    if (!handleSeek(e.target.currentTime)) {
      e.target.currentTime = currentTime
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  if (!video) {
    return <div className="text-center text-gray-500">Video not found</div>
  }

  return (
    <div className="max-w-6xl mx-auto p-6">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">{video.title}</h1>
        <p className="text-gray-600">{video.description}</p>
      </div>

      <div className="bg-black rounded-lg overflow-hidden mb-6">
        <video
          ref={videoRef}
          src={video.video_url}
          onTimeUpdate={handleTimeUpdate}
          onSeeked={handleSeeked}
          controls={!isBlocked}
          className="w-full h-auto"
          preload="metadata"
        />
      </div>

      <ProgressBar 
        progress={progress}
        questions={questions}
        currentTime={currentTime}
        duration={video.duration}
      />

      <QuestionModal
        isOpen={showModal}
        question={currentQuestion}
        onSubmit={handleAnswerSubmit}
        onClose={() => {
          setShowModal(false)
          setIsBlocked(false)
        }}
      />
    </div>
  )
}

export default VideoPlayer
