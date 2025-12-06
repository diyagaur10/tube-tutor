import React, { useState } from 'react'
import { X, CheckCircle, AlertCircle } from 'lucide-react'

const QuestionModal = ({ isOpen, question, onSubmit, onClose }) => {
  const [answer, setAnswer] = useState('')
  const [selectedOption, setSelectedOption] = useState('')
  const [showExplanation, setShowExplanation] = useState(false)

  if (!isOpen || !question) return null

  const handleSubmit = (e) => {
    e.preventDefault()
    const finalAnswer = question.question_type === 'mcq' ? selectedOption : answer
    if (finalAnswer.trim()) {
      onSubmit(finalAnswer)
      setAnswer('')
      setSelectedOption('')
      setShowExplanation(false)
    }
  }

  const renderQuestionContent = () => {
    switch (question.question_type) {
      case 'mcq':
        return (
          <div className="space-y-3">
            {question.options?.map((option, index) => (
              <label key={index} className="flex items-center space-x-3 cursor-pointer">
                <input
                  type="radio"
                  name="option"
                  value={option}
                  checked={selectedOption === option}
                  onChange={(e) => setSelectedOption(e.target.value)}
                  className="w-4 h-4 text-primary-600"
                />
                <span className="text-gray-700">{option}</span>
              </label>
            ))}
          </div>
        )
      
      case 'fill_in':
        return (
          <div>
            <p className="text-gray-700 mb-3">{question.question_text}</p>
            <input
              type="text"
              value={answer}
              onChange={(e) => setAnswer(e.target.value)}
              placeholder="Fill in the blank..."
              className="input-field"
            />
          </div>
        )
      
      case 'one_word':
        return (
          <div>
            <p className="text-gray-700 mb-3">{question.question_text}</p>
            <input
              type="text"
              value={answer}
              onChange={(e) => setAnswer(e.target.value)}
              placeholder="Your answer..."
              className="input-field"
            />
          </div>
        )
      
      default:
        return <p className="text-gray-700">{question.question_text}</p>
    }
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-lg font-semibold text-gray-900">
            Question: {question.question_text}
            {/* Question at {Math.floor(question.timestamp / 60)}:{(question.timestamp % 60).toFixed(0).padStart(2, '0')} */}
          </h3>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600"
          >
            <X size={24} />
          </button>
        </div>

        <div className="mb-6">
          {renderQuestionContent()}
        </div>

        <div className="flex space-x-3">
          <button
            onClick={handleSubmit}
            disabled={question.question_type === 'mcq' ? !selectedOption : !answer.trim()}
            className="btn-primary flex-1 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Submit Answer
          </button>
          <button
            onClick={onClose}
            className="btn-secondary"
          >
            Skip
          </button>
        </div>

        {question.explanation && (
          <div className="mt-4 p-3 bg-blue-50 rounded-lg">
            <div className="flex items-start space-x-2">
              <CheckCircle className="w-5 h-5 text-blue-600 mt-0.5" />
              <p className="text-sm text-blue-800">{question.explanation}</p>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default QuestionModal
