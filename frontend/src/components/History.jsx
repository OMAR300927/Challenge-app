import Navbar from './Navbar'
import { useEffect, useState } from 'react'
import { api } from '../utils/api'
import { Check } from 'lucide-react'

const History = () => {
  const [userHistory, setUserHistory] = useState(null);

  useEffect(() => {
    const allChallenges = async () => {
      try {
        const response = await api.get('/challenges/all-challenges');
        setUserHistory(response.data);
      } catch (e) {
        console.log(e)
      }
    }

    allChallenges()
  }, [])

  return (
    <div className="page-background min-h-screen">
      <Navbar />
      <div className='flex flex-col items-center mx-5'>
        <h2 className='text-white text-3xl sm:text-4xl md:text-5xl font-bold mt-23'>History</h2>
        <div className='history-container'>
          <div className='m-4'>
            {!userHistory ? <p className='text-gray-200 text-2xl sm:text-3xl font-[650]'>You didn't create any challenges yet.</p>
              : <div className='text-gray-200 text-2xl sm:text-3xl font-[650] space-y-4'>
                {userHistory.map((challenge, index) => (
                  <div
                    key={index}
                    className='space-y-3'
                  >
                    <h3>- {challenge.question}</h3>

                    {challenge.options.map((option, optionIndex) => (
                      <p
                        key={optionIndex}
                        className='flex items-center gap-4'
                      >
                        - {option}
                        {optionIndex === Number(challenge.correct_answer) && (
                          <Check className='text-green-500' size={30} strokeWidth={5}/>
                        )}
                      </p>
                    ))}

                    <p>- {challenge.explanation}</p>
                    <hr className='border-black/50 border-t-2 w-100 mt-8' />

                  </div>
                ))}
              </div>}
          </div>
        </div>
      </div>
    </div>
  )
}

export default History