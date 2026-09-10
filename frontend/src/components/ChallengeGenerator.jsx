import { useState, useEffect } from "react"
import { api } from '../utils/api'
import { LoaderCircle } from 'lucide-react';

const ChallengeGenerator = () => {
  const [quota, setQuota] = useState(0);
  const [currentQuestion, setCurrentQuestion] = useState(null);
  const [selectedOption, setSelectedOption] = useState(null);
  const [quotaResetAt, setQuotaResetAt] = useState(null);
  const [loading, setLoading] = useState(false);


  useEffect(() => {
    const userQuota = async () => {
      try {
        const response = await api.get('/users/get-quota')

        setQuota(response.data.quota)
        setQuotaResetAt(response.data.quota_reset_at)
      } catch (e) {
        console.log(e)
      }
    }

    userQuota()
  }, [])

  useEffect(() => {
    if (!quotaResetAt) {
      return;
    }

    const resetTime = new Date(quotaResetAt).getTime();
    const now = Date.now();

    const delay = resetTime - now;

    const resetQuota = async () => {
      try {
        const response = await api.post('/users/reset-quota');

        setQuota(response.data.quota);
        setQuotaResetAt(response.data.quota_reset_at);
      } catch (e) {
        console.log(e)
      }
    }

    if (delay <= 0) {
      resetQuota();
      return;
    }

    const timer = setTimeout(() => {
      resetQuota();
    }, delay);

    return () => clearTimeout(timer)
  }, [quotaResetAt])

  const getQuestion = async () => {
    if (quota === 0) {
      return;
    }

    try {
      setLoading(true)
      const response = await api.post(
        '/challenges/create'
      )
      setCurrentQuestion(response.data)
      setSelectedOption(null)
      setQuota(prev => prev - 1);
    } catch (e) {
      console.log(e)
    } finally {
      setLoading(false);
    }
  }

  const getOptionClass = (index) => {
    if (selectedOption === null) {
      return '';
    }

    if (index === Number(currentQuestion.correct_answer)) {
      return 'correct';
    }

    if (index === selectedOption) {
      return 'wrong';
    }

    return '';
  }

  return (
    <div className="app-container">
      <div className="flex flex-col items-center mt-8">
        <h2 className="text-white text-2xl sm:text-3xl font-bold">Your remaining credits: {quota}</h2>
        <hr className='border-black/50 border-t-2 w-100 mt-4' />
        {loading && quota !== 0 && (
          <span className="flex items-center justify-center gap-2 text-white font-medium text-lg sm:text-2xl mt-3">
            <LoaderCircle className="animate-spin" size={20} />
            wait for generating the challenge...
          </span>
        )}

        {currentQuestion && (
          <div className="text-white px-7 mt-6 text-lg sm:text-xl font-semibold">
            <h2>{currentQuestion.question}</h2>
            <ul className="mt-3 space-y-4">
              {currentQuestion.options.map((option, index) => (
                <li
                  key={index}
                  className={`mb-3 p-3 bg-indigo-600 border border-gray-400 rounded-2xl cursor-pointer hover:scale-102 transition duration-300 ${getOptionClass(index)}`}
                  onClick={() => {
                    if (selectedOption === null) {
                      setSelectedOption(index);
                    }
                  }}
                >
                  {option}
                </li>
              ))}
            </ul>
            {selectedOption !== null && (
              <p>
                {currentQuestion.explanation}
              </p>
            )}
          </div>
        )}

        <button
          className="bg-indigo-700 p-4 text-white font-semibold text-xl sm:text-2xl rounded-2xl mt-4 cursor-pointer transition duration-300 active:scale-95"
          onClick={getQuestion}
          disabled={loading}
        >
          {loading ? 'Generating...' : 'Generate Challenge'}
        </button>
      </div>
    </div>
  )
}

export default ChallengeGenerator