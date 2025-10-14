import React from 'react'
import { Play, CheckCircle, Clock } from 'lucide-react'

const ProgressBar = ({ progress, questions, currentTime, duration }) => {
  const completedCount = progress.completed_questions?.length || 0
  const totalQuestions = questions.length
  const progressPercentage = duration ? (currentTime / duration) * 100 : 0

  return (
    <div className="bg-white rounded-lg p-6 shadow-md">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-900">Progress</h3>
        <div className="flex items-center space-x-4 text-sm text-gray-600">
          <div className="flex items-center space-x-1">
            <CheckCircle className="w-4 h-4 text-green-600" />
            <span>{completedCount}/{totalQuestions} Questions</span>
          </div>
          <div className="flex items-center space-x-1">
            <Clock className="w-4 h-4 text-blue-600" />
            <span>{Math.floor(currentTime / 60)}:{(currentTime % 60).toFixed(0).padStart(2, '0')}</span>
          </div>
        </div>
      </div>

      {/* Video Progress */}
      <div className="mb-4">
        <div className="flex justify-between text-sm text-gray-600 mb-1">
          <span>Video Progress</span>
          <span>{Math.floor(currentTime / 60)}:{(currentTime % 60).toFixed(0).padStart(2, '0')} / {duration ? `${Math.floor(duration / 60)}:${(duration % 60).toFixed(0).padStart(2, '0')}` : '--:--'}</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div 
            className="bg-primary-600 h-2 rounded-full transition-all duration-300"
            style={{ width: `${progressPercentage}%` }}
          />
        </div>
      </div>

      {/* Question Timeline */}
      {questions.length > 0 && (
        <div>
          <h4 className="text-sm font-medium text-gray-700 mb-2">Question Timeline</h4>
          <div className="space-y-2">
            {questions.map((question, index) => {
              const isCompleted = progress.completed_questions?.includes(question.id)
              const isUpcoming = question.timestamp > currentTime
              const isCurrent = Math.abs(question.timestamp - currentTime) < 5
              
              return (
                <div 
                  key={question.id}
                  className={`flex items-center space-x-3 p-2 rounded-lg ${
                    isCompleted 
                      ? 'bg-green-50 border border-green-200' 
                      : isCurrent 
                        ? 'bg-blue-50 border border-blue-200'
                        : isUpcoming
                          ? 'bg-gray-50 border border-gray-200'
                          : 'bg-yellow-50 border border-yellow-200'
                  }`}
                >
                  <div className={`w-3 h-3 rounded-full ${
                    isCompleted 
                      ? 'bg-green-500' 
                      : isCurrent 
                        ? 'bg-blue-500'
                        : isUpcoming
                          ? 'bg-gray-400'
                          : 'bg-yellow-500'
                  }`} />
                  <div className="flex-1">
                    <div className="flex items-center justify-between">
                      <span className="text-sm font-medium text-gray-900">
                        Question {index + 1}
                      </span>
                      <span className="text-xs text-gray-500">
                        {Math.floor(question.timestamp / 60)}:{(question.timestamp % 60).toFixed(0).padStart(2, '0')}
                      </span>
                    </div>
                    <p className="text-xs text-gray-600 truncate">
                      {question.question_text}
                    </p>
                  </div>
                  {isCompleted && (
                    <CheckCircle className="w-4 h-4 text-green-600" />
                  )}
                </div>
              )
            })}
          </div>
        </div>
      )}
    </div>
  )
}

export default ProgressBar
