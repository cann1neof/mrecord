<template>
    <div class="d-flex flex-column">
        <div class="container-transparent mx-auto mb-0 pb-0 d-flex justify-space-between">
            <div>
                <mrd-button to='/my/' dark > 
                    <v-icon> mdi-chevron-left </v-icon> Назад
                </mrd-button>
            </div>
            <div>
                <mrd-button @click="auth()" dark color="#D96906" > 
                    Подтвердить <v-icon> mdi-chevron-right </v-icon>
                </mrd-button>
            </div>

        </div>

        <v-card width="600px" class=" mx-auto mt-12 pa-10" color="#013AAA" dark>       
            <v-form ref="userInfo" v-model="valid" >
                <p>
                    Давайте знакомиться! Представитьесь, пожалуйста.
                </p>

                <v-text-field
                    outlined
                    v-model="last_name"
                    label="Фамилия"
                    :rules="[v => !!v || 'Это поле обязательно для заполнения']"
                    required
                ></v-text-field>

                <v-text-field
                    outlined
                    v-model="first_name"
                    label="Имя"
                    required
                    :rules="[v => !!v || 'Это поле обязательно для заполнения']"
                ></v-text-field>

                <v-text-field
                    outlined
                    v-model="second_name"
                    label="Отчество (при наличии)"
                ></v-text-field>

                <v-text-field
                    outlined
                    v-model="username"
                    :counter="24"
                    :rules="loginRules"
                    label="Логин"
                    @click="uniqLogin = true"
                    required
                ></v-text-field>

                <v-text-field
                    outlined
                    v-model="password1"
                    :rules="[v => !!v || 'Это поле обязательно для заполнения']"
                    label="Пароль"
                    required
                    type="password"
                ></v-text-field>

                <v-text-field
                    outlined
                    v-model="password2"
                    label="Повторите пароль"
                    required
                    type="password"
                    :rules="[v => !!v || 'Это поле обязательно для заполнения']"
                ></v-text-field>

                <v-checkbox
                    v-model="id_exists"
                    label="У меня есть жетон MRecord Plus"
                ></v-checkbox>

                <v-checkbox
                    v-model="checkbox"
                    :rules="[v => !!v || 'Согласитесь, тобы продолжить']"
                    label="Я согласен на обработку моих персональных данных"
                    required
                ></v-checkbox>
            </v-form>
        </v-card>

         <v-card width="600px" class=" mx-auto mt-12 pa-10" color="#013AAA" dark v-if="id_exists">       
            <v-form ref="mrdInfo" v-model="valid" >
                <p>
                    Замечательно, что у Вас есть жетон MRecord Plus! Привяжите его к своей учетной записи.
                </p>
                <v-text-field
                    outlined
                    v-model="id"
                    :counter="6"
                    :rules="idRules"
                    label="MRecordID"
                    required
                ></v-text-field>

                <v-text-field
                    outlined
                    v-model="code"
                    :counter="8"
                    :rules="codeRules"
                    label="Код подтверждения"
                    required
                ></v-text-field>
            </v-form>
        </v-card>

        <v-card width="600px" class=" mx-auto mt-12 pa-10" color="#013AAA" dark>       
            <v-form ref="personalInfo" v-model="valid" >
                <p>
                    Расскажите нам о себе
                </p>
                <v-text-field
                    outlined
                    v-model="insuranse"
                    type="number"
                    :counter="16"
                    label="Страховой номер"
                    :rules="[v => !!v || 'Это поле обязательно для заполнения']"
                    required
                ></v-text-field>

                <v-text-field
                    outlined
                    v-model="email"
                    :rules="emailRules"
                    label="Email"
                    @click="uniqEmail = true"
                    required
                ></v-text-field>

                <VuePhoneNumberInput
                    required
                    @update="updatePhone" 
                    v-model="p" 
                    :translations="translations"
                    dark
                    dark-color="#013AAA"
                    @click="uniqPhone = true"
                />

                <v-subheader color="error">{{uniqPhone ? '' : 'Пользователь с таким номером телефона уже существует'}}</v-subheader>

                <v-select
                    v-model="bloodType"
                    :items="[ '0(I)', 'A(II)', 'B(III)', 'AB(IV)' ]"
                    required
                    label="Группа крови"
                    :rules="[v => !!v || 'Это поле обязательно для заполнения']"
                ></v-select>

                <v-select
                    v-model="rhesusFactor"
                    :items="[ 'Rh+', 'Rh-' ]"
                    label="Резус фактор"
                    required
                    type="password"
                    :rules="[v => !!v || 'Это поле обязательно для заполнения']"
                ></v-select>
            </v-form>
        </v-card>

        <v-card width="600px" class=" mx-auto mt-12 pa-10" color="#013AAA" dark>       
            <v-form ref="illnessesInfo">
                <p>
                    Расскажите нам о Ваших диагностированных заболеваниях.
                </p>
                <illnesses-viewer :instance="illnesses" :landscape="true" @add="addI($event)" @del="delI($event)"></illnesses-viewer>
            </v-form>
        </v-card>

        <v-card width="600px" class=" mx-auto mt-12 pa-10" color="#013AAA" dark>       
            <v-form ref="recipesInfo">
                <p>
                    Расскажите нам о принимаемых Вами лекартсвенных препаратах.
                </p>
                <recipes-viewer :instance="recipes" :landscape="true" @add="addR($event)" @del="delR($event)"></recipes-viewer>
            </v-form>
        </v-card>


        <v-card width="600px" class=" mx-auto mt-12 pa-10" color="#013AAA" dark>       
            <v-form ref="relativeInfo">
                <p>
                    Укажите контакты своих близких, которых необходимо информировать о Вашем попадании в больницу.
                </p>
                <contacts-viewer :instance="contacts" @add="addC($event)" @del="delC($event)"></contacts-viewer>
            </v-form>
        </v-card>
    </div>

</template>

<script>
import mrdButton from '../components/mrdButton.vue'
import recipesViewer from '../components/recipesViewer.vue'
import illnessesViewer from '../components/illnessesViewer.vue'
import contactsViewer from '../components/contactsViewer.vue'
import VuePhoneNumberInput from 'vue-phone-number-input';
import 'vue-phone-number-input/dist/vue-phone-number-input.css';

export default {
    data : ()=> ({
        valid: true,
        checkbox: false,
        id_exists: false,
        email: '',
        username : '',
        first_name : '',
        second_name : '',
        last_name : '',
        password1 : '',
        password2 : '',
        id : '',
        code : '',
        insuranse : '',
        bloodType : '',
        rhesusFactor : '',
        phone: '',
        country: '',
        p : '',
        validId : true,
        validCode : true,

        illnesses : [],
        recipes : [],
        contacts : [],
        uniqLogin : true,
        uniqEmail: true,
        uniqPhone: true,

        translations:{
            countrySelectorLabel: 'Код страны',
            countrySelectorError: 'Выберите код страны',
            phoneNumberLabel: 'Введите номер телефона',
            example: 'Например:'
        },
    }),
    components : {
        mrdButton,
        recipesViewer,
        illnessesViewer,
        contactsViewer, 
        VuePhoneNumberInput,
    },
    methods: {
        async auth(){
            if(this.$refs.userInfo.validate() && this.$refs.personalInfo.validate() && this.phone && this.country){
                const sha256 = require('sha256')
                let salt = '', outputData = {}
                
                await this.$axios.get( this.$store.getters.url + 'register/' )
                    .then( res => {
                        salt = res.data.salt
                    } )
                const password = sha256(this.password1 + salt)
                const saltedPassword = salt + '$' + password

                outputData['usr'] = {
                    'password' : saltedPassword,
                    'username' : this.username,
                    'email' : this.email,
                    'first_name' : this.first_name,
                    'last_name' : this.last_name,
                    'second_name':this.second_name,
                    'telephone' : this.phone,
                    'country_code' : this.country,
                }

                outputData['rec'] = {
                    'insurance_number' : this.insuranse,
                    'blood_type' : this.bloodType + ' ' + this.rhesusFactor,
                    'illnesses' : JSON.stringify( this.illnesses ),
                    'recipes' : JSON.stringify( this.recipes ),
                    'children' : '[]',
                    'contacts' : JSON.stringify( this.contacts ),
                }
                
                outputData['id_exists'] = false

                if(this.id_exists){
                    outputData['id_exists'] = true
                    outputData['mrd'] = {
                        'id' : this.id,
                        'code' : this.code
                    }
                }
                console.log(outputData)
                this.$axios.post( this.$store.getters.url + 'register/', outputData)
                .then(async res => {
                    if(res.status == 200){
                        await this.$store.dispatch('saveToken', res.data.token)
                        await this.$store.dispatch('createUserInfo',{salt: salt, password: password, username: this.username } )
                        await this.$store.dispatch('logIn')
                        this.$router.push('/my')
                    }
                    if(res.status == 208){
                        if(res.data.error == 'userNameError'){
                            this.uniqLogin = false
                        }
                        if(res.data.error == 'emailError'){
                            this.uniqEmail = false
                        }
                        if(res.data.error == 'telephoneError'){
                            this.uniqPhone = false
                        }
                    }
                }).catch(err => { 
                    if(err.response.status == 403){
                        this.validId = false
                        this.validCode = false
                    }
                    if(err.response.status == 400){
                        this.valid = false
                    }
                })
            }
        },
        updatePhone(payload){
            if(payload.isValid){
                this.phone = payload.nationalNumber
                this.country = payload.countryCallingCode
            }
        },

        delR(index ){
            this.recipes.splice(index, 1)
        },
        delI(index ){
            this.illnesses.splice(index, 1)
        },
        delC(index ){
            this.contacts.splice(index, 1)
        },
        delCh(index ){
            this.children.splice(index, 1)
        },

        addR(data ){
            this.recipes.push(data)
        },
        addI(data ){
            this.illnesses.push(data)
        },
        addC(data ){
            this.contacts.push(data)
        },
        addCh(data ){
            this.children.push(data)
        },
        
    },
    computed:{
        idRules() {
            const rules  =  []
            if(this.validId){
                const rule = [
                    v => !!v || 'Необходимо ввести MRecordID',
                    v => (v && v.length <= 6) || 'Слишком длинный ID. Максимум - 6 символов!',
                    v => (v && this.validId) || 'Проверьте правильность написания MRecordID'
                ]
                rules.push(rule)
            }
            return rules
        },
        codeRules() {
            const rules  =  []
            if(this.validCode){
                const rule = [
                    v => !!v || 'Необходимо ввести код подтверждения',
                    v => (v && v.length <= 8) || 'Слишком длинный код. Максимум - 8 символов!',
                    v => (v && this.validCode) || 'Проверьте правильность написания кода подтвержения'
                ]
                rules.push(rule)
            }
            return rules
        },
        loginRules(){        
            return [
                v => !!v || 'Необходимо ввести логин',
                v => (v && v.length <= 24) || 'Слишком длинный логин. Максимум - 10 символов!',
                v => (v && this.uniqLogin) || 'Пользователь с таким логином уже существует'
            ]
        },
        emailRules(){
            return [
                v => !!v || 'Необходимо ввести email',  
                v => /.+@.+\..+/.test(v) || 'Неправильный email',
                v => (v && this.uniqEmail) || 'Пользователь с таким E-Mail уже существует'
            ] 
        },
    },
    watch: {
        $route(){
            if(this.$store.getters.status){
                this.$router.push('/my')
            }
        },
    }
}
</script>

<style>
.container-transparent{
    background-color: transparent;
    padding: 20px 15px;
    margin-bottom: 12px;
    box-sizing: border-box;
    color: #505050;
    font-weight: bold;
    border-radius: 7px;
    width: 750px;
    vertical-align: bottom;
}
.main-title{
    font-size: 37px;
    color: #404040;
    text-align: center;
}

/* Chrome, Safari, Edge, Opera */
input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

/* Firefox */
input[type=number] {
  -moz-appearance: textfield;
}

</style>
