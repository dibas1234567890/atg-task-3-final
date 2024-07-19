import axios from "axios";

export const getUserType = async () => {
  const token = localStorage.getItem('access_token'); 

  try {
    const response = await axios.get('http://127.0.0.1:8000/api/user-obj', {
      headers: {
        'Authorization': `Bearer ${token}`
      },
      withCredentials: true
    });

    const data = response.data;
    console.log(data.user_type);
    return data.user_type;
  } catch (error) {
    console.error('Error fetching user type:', error);
    return null;
  }
};
