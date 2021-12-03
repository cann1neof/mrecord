import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    cart: null,
    user : {
      'username' : '',
      'password' : '',
      'last_name' : '',
      'first_name' : '',
      'second_name' : '',
      'email' : '',
      'salt' : '',
      'telephone' : '',
    },
    record : {
      'serial_number' : '',
      'insurance_number' : '',
      'blood_type' : '',
      'illnesses' : [],
      'contacts' : [],
      'hospitals' : [],
      'recipes' : [],
      'children' : [],
    },
    is_logged: false,
    url: '/api/',
    //url: 'mrecord.dqpig.ml/api/',
    token : '',
    m_token : '',
  },
  mutations: {
    setUserInfo(state, data){
      for(let key in state.user){
        if(data[key]){
          state.user[key] = data[key]
        }
      }
    },
    setRecordInfo(state, data){
      for(let key in state.record){
        if(data[key]){
          state.record[key] = data[key]
        }
      }
    },
    logOut(state){
      state.user = {
        'username' : '',
        'password' : '',
        'last_name' : '',
        'first_name' : '',
        'second_name' : '',
        'email' : '',
        'salt' : '',
      }
      state.record = {
        'serial_number' : '',
        'insurance_number' : '',
        'blood_type' : '',
        'illnesses' : [],
        'contacts' : [],
        'hospitals' : [],
        'recipes' : [],
        'children' : [],
      }
      state.is_logged = false
    },
    logIn(state){
      state.is_logged = true
    },
    saveToken(state, t){
      state.token = t
    },
    setNewPassword(state, data){
      state.user.password = data.password
      state.user.salt = data.salt
    },
    setMigrationToken(state, t){
      state.m_token = t
    },
    saveCart(state, data){
      if(!state.cart)
        state.cart = data
      else{
        for(let each of data){
          const currentCart = state.cart.find(el => el.model == each.model && el.selected == each.selected)
          if(currentCart){
            currentCart.quantity += (each.quantity - currentCart.quantity)
          }
          else{
            state.cart.push(data)
          }
        }
      }
    },
    updateCart(state, data){
      state.cart = data.length ? data : null
    }
  },
  actions: {
    createUserInfo({commit}, data){
      commit('setUserInfo', data)
    },
    createRecordInfo({commit}, data){
      if(data.contacts  != '' && data.contacts   != undefined && !Array.isArray(data.contacts)){
        data.contacts = JSON.parse(data.contacts)
      } 
      else if(data.contacts == '' || data.contacts == undefined){
        data.contacts = []
      }
      if(data.hospitals != '' && data.hospitals  != undefined && !Array.isArray(data.hospitals) ){
        data.hospitals = JSON.parse(data.hospitals)
      } 
      else if(data.hospitals == '' || data.hospitals == undefined){
        data.hospitals = []
      }
      if(data.recipes   != '' && data.recipes    != undefined && !Array.isArray(data.recipes)   ){
        data.recipes = JSON.parse(data.recipes) 
      } 
      else if(data.recipes == '' || data.recipes == undefined){
        data.recipes = []
      }
      if(data.children  != '' && data.children   != undefined && !Array.isArray(data.children)  ){
        data.children = JSON.parse(data.children)
      } 
      else if(data.children == '' || data.children == undefined){
        data.children = []
      }
      if(data.illnesses != '' && data.illnesses  != undefined && !Array.isArray(data.illnesses) ){
        data.illnesses = JSON.parse(data.illnesses)
      } 
      else if(data.illnesses == '' || data.illnesses == undefined){
        data.illnesses = []
      }

      commit('setRecordInfo', data)
    },
    logOut({commit}){
      commit('logOut')
    },
    logIn({commit}){
      commit('logIn')
    },
    saveToken({commit}, t){
      commit('saveToken', t)
    },
    setNewPassword({commit}, data){
      commit('setNewPassword', data)
    },
    setMigrationToken({commit}, t){
      commit('setMigrationToken', t)
    },
    saveCart({commit}, data){
      commit('saveCart', data)
    },
    updateCart({commit}, data){
      commit('updateCart', data)
    }
  },
  getters: {
    password : state => state.user.password,
    username : state => state.user.username,
    salt : state => state.user.salt,
    user : state => state.user,
    record : state => state.record,
    url : state => state.url,
    status : state => state.is_logged,
    token : state => state.token,
    m_token : state => state.m_token,
    cart : state => state.cart,
  }
})
