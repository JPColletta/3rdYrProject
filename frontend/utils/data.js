import { api } from "../libs/api.js"

export default {
	getNow: async () => {
       return api(({
	      method: 'GET',
	      endpoint: `/welcome`,
	      usingAuthToken: true,
	    }).catch(error => {
	      // Validation errors
	      if (error.status === 400 || error.status === 404) {
	        return Promise.reject({ validationErrors: error.body });
	      }
	      throw error;
	    }));
	}
}