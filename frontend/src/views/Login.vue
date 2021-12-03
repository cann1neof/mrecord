<template>
    <div class="d-flex justify-center">
        <v-card width="600px" class="mt-12" color="#013AAA" dark>
            <v-card-title>
                Войдите в аккаунт с помошью:
            </v-card-title>
            <v-card-subtitle>
                <h3 style="color: #f11" class="my-2">{{LoginError}}</h3>
            </v-card-subtitle>
            <v-card-text>
                <v-tabs
                    background-color="#013AAA" dark
                    class=""
                    v-model="tab"
                >
                    <v-tab :href="'#username'">
                        Логина
                    </v-tab>
                    <v-tab :href="'#email'">
                        Электронной почты
                    </v-tab>
                    <v-tab :href="'#phone'">
                        Телефона
                    </v-tab>
                    <v-tab-item :value="'username'">
                        <v-card flat tile color="#013AAA" dark>
                            <v-card-text>
                                <v-text-field
                                    outlined
                                    v-model="username"
                                    label="Введите имя пользователя"
                                    required
                                    hide-details=""
                                ></v-text-field>
                                <v-text-field
                                    outlined
                                    v-model="password"
                                    label="Введите пароль"
                                    type="password"
                                    required
                                    class="mt-3"
                                    hide-details=""
                                ></v-text-field>
                            </v-card-text>
                        </v-card>
                    </v-tab-item>
                    <v-tab-item :value="'email'">
                        <v-card flat tile color="#013AAA" dark>
                             <v-card-text>
                                <v-text-field
                                    outlined
                                    v-model="email"
                                    label="Введите электронную почту"
                                    :rules="emailRules"
                                    required
                                    hide-details=""
                                ></v-text-field>
                                <v-text-field
                                    outlined
                                    v-model="password"
                                    label="Введите пароль"
                                    type="password"
                                    required
                                    class="mt-3"
                                    hide-details=""
                                ></v-text-field>
                            </v-card-text>
                        </v-card>
                    </v-tab-item>
                    <v-tab-item :value="'phone'">
                        <v-card flat tile color="#013AAA" dark>
                            <v-card-text>
                                <VuePhoneNumberInput
                                    required
                                    @update="updatePhone" 
                                    v-model="p" 
                                    :translations="translations"
                                    dark
                                    dark-color="#013AAA"
                                />
                                <v-text-field
                                    outlined
                                    v-model="password"
                                    label="Введите пароль"
                                    type="password"
                                    required
                                    class="mt-3"
                                    hide-details=""
                                ></v-text-field>
                            </v-card-text>
                        </v-card>
                    </v-tab-item>
                </v-tabs>
            </v-card-text>

            <v-card-actions>
                <mrd-button @click="authenticate()"  color="#D96906" dark>
                    Войти
                </mrd-button>

                <mrd-button to="/register/" color="#D96906" class="ml-2" dark>
                    Регистрация
                </mrd-button>
            </v-card-actions>
        </v-card>
    </div>
</template>

<script>
import mrdButton from '../components/mrdButton.vue'
import VuePhoneNumberInput from 'vue-phone-number-input';
import 'vue-phone-number-input/dist/vue-phone-number-input.css';

export default {
    data : ()=> ({
        username : '',
        password : '',
        email: '',
        p: '',
        county: '',
        phone: '',
        valid : true,
        tab: '',
        translations:{
            countrySelectorLabel: 'Код страны',
            countrySelectorError: 'Выберите код страны',
            phoneNumberLabel: 'Введите номер телефона',
            example: 'Например:'
        },
    }),
    components : {
        mrdButton,
        VuePhoneNumberInput,
    },
    methods: {
        authenticate(){
            const sha256 = require('sha256')
            let outputData = {}
            if(this.tab === 'username' && this.username)    outputData =  {'username': this.username}
            else if(this.tab === 'email' && this.email)     outputData = {'email': this.email}
            else if(this.tab === 'phone' && this.phone)     outputData = {'phone': this.phone}

            this.$axios.post( this.$store.getters.url + 'startauthsession/', outputData).then( res => {
                if (res.status == 200){
                    const token = res.data.token
                    
                    const salt = res.data.salt

                    const password = sha256(this.password + salt)

                    this.$axios.post( this.$store.getters.url + 'authorize/', { 'token': token, 'password': password } )
                    .then( res=>{    
                        if(res.status == 200){
                            this.$store.dispatch('createUserInfo', {'username': this.username, 'password': password, 'salt': salt})
                            this.$store.dispatch('saveToken', token)
                            this.$store.dispatch('logIn')
                            this.$router.push('/my')
                        }
                    }).catch(err => {
                        if(err.response.status == 403){
                            this.valid = false
                        }
                        if(err.response.status == 401){
                            this.$emit('raise', {errCode: 'CV02', errMessage: 'Ошибка авторизации.'})
                            this.authenticate()
                        }
                    })
                }
                
            }).catch(err => {
                if(err.response.status==404){
                    this.valid = false
                }else{
                    console.log(err)
                }
            })
        },
        updatePhone(payload){
            if(payload.isValid){
                this.phone = payload.nationalNumber
                this.country = payload.countryCallingCode
            }
        },
    },
    computed:{
        LoginError(){
            return !this.valid ? 'Неправильный логин или пароль' : ''
        },
        emailRules(){
            return [
                v => !!v || 'Необходимо ввести email',  
                v => /.+@.+\..+/.test(v) || 'Неправильный email',
            ] 
        },
    }
}
</script>
