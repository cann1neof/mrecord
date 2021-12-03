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
                    v-model="username"
                    :counter="24"
                    :rules="loginRules"
                    label="Логин"
                    required
                ></v-text-field>

                <v-text-field
                    v-model="password1"
                    :rules="passwordRules"
                    label="Пароль"
                    required
                    type="password"
                ></v-text-field>

                <v-text-field
                    v-model="password2"
                    label="Повторите пароль"
                    required
                    type="password"
                ></v-text-field>
                
                <v-text-field
                    v-model="email"
                    :rules="emailRules"
                    label="Email"
                    required
                ></v-text-field>
                
                <v-row>
                    <v-col cols=6>
                        <v-select
                            v-model="country"
                            :items="countryChoices"
                            label="Код страны"
                            prepend-icon="mdi-phone"
                            :hint="country.state ? `${country.state}, ${country.text} ` : ''"
                            required
                            single-line
                            return-object
                            persistent-hint
                        >
                        </v-select>
                    </v-col>

                    <v-col cols=6>
                        <v-text-field
                            v-model="phone"
                            label="Номер телефона"
                            type="number"
                            required
                        ></v-text-field>
                    </v-col>

                </v-row>

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
                    v-model="id"
                    :counter="6"
                    :rules="idRules"
                    label="MRecordID"
                    required
                ></v-text-field>

                <v-text-field
                    v-model="code"
                    :counter="8"
                    :rules="codeRules"
                    label="Код подтверждения"
                    required
                ></v-text-field>
            </v-form>
        </v-card>
        <v-card width="600px" class=" mx-auto mt-12 pa-10" color="#013AAA" dark>       
            <v-form ref="relativeInfo">
                <p>
                    Кому звонить если *тьфу-тьфу-тьфу* что-то случится?
                </p>
                <contacts-viewer :instance="contacts" @add="addC($event)" @del="delC($event)"></contacts-viewer>
            </v-form>
        </v-card>
    </div>

</template>

<script>
import mrdButton from '../components/mrdButton.vue'
import contactsViewer from '../components/contactsViewer.vue'

export default {
    props: ['id'],
    data : ()=> ({
        valid: true,
        checkbox: false,
        id_exists: false,
        email: '',
        username : '',
        password1 : '',
        password2 : '',
        code : '',
        contacts : [],

        country: {value: null, text: 'Выберете код страны', state: ''} ,
        countryChoices : [ 
            {value: '7', text: '+7', state: 'Russia'} 
        ],

        loginRules:
        [
            v => !!v || 'Необходимо ввести логин',
            v => (v && v.length <= 24) || 'Слишком длинный логин. Максимум - 10 символов!',
        ],

        emailRules:
        [
            v => !!v || 'Необходимо ввести email',  
            v => /.+@.+\..+/.test(v) || 'Неправильный email',
        ], 
    }),
    components : {
        mrdButton,
        contactsViewer, 
    },
    methods: {
        async auth(){
            if( this.$refs.userInfo.validate() ){

                const sha256 = require('sha256')
                let salt = ''

                await this.$axios.get( this.$store.getters.url + 'register/' )
                .then( res => {
                    salt = res.data.salt
                } )
                
                const password = salt + '$' + sha256( this.password1 + salt )

                if(this.id_exists){
                    this.authPlus(password)
                }
                else{
                    this.authMinus(password)
                }
            }
        },
        async authPlus(pwd){
            console.log()
            const data = {
                id_exists: true,
                id: this.id,
                code: this.code,
                username: this.username,
                password: pwd,
                email: this.email,
                token: this.$store.getters.m_token,
                contacts: JSON.stringify(this.contacts)
            }

            this.$axios.post( this.$store.getters.url + 'migrate/', data).then(res => {
                if(res.status==201){
                    this.$router.push('/my')
                }
            }).catch(err => {
                if(err.response.status==401){
                    this.$emit('raise', [{errCode: 'CV01', errMessage: 'Ошибка в составлении запроса. Попробуйте еще раз. В случае повторной ошибки обратитесь в службу поддержки'}])
                    this.$router.push('/my/settings')
                }
            })
        },
        async authMinus(pwd){

            const data = {
                id_exists: false,
                username: this.username,
                password: pwd,
                email: this.email,
                token: this.$store.getters.m_token,
                contacts: JSON.stringify(this.contacts)
            }
            
            this.$axios.post( this.$store.getters.url + 'migrate/', data).then(res => {
                if(res.status==201){
                    this.$router.push('/my')
                }
            }).catch(err => {
                if(err.response.status==401){
                    this.$emit('raise', {errCode: 'CV01', errMessage: 'Ошибка в составлении запроса. Попробуйте еще раз. В случае повторной ошибки обратитесь в службу поддержки'})
                    this.$router.push('/my/settings')
                }
            })
        },

        delC(index ){
            this.contacts.splice(index, 1)
        },
        addC(data ){
            this.contacts.push(data)
        },
    },
    computed:{
        passwordRules(){
            const rules = []
            if (this.password2) {
                const rule =
                    v => (!!v && v) === this.password2 ||
                    'Пароли не совпадают'
                rules.push(rule)
            }
            return rules
        },
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
    },
    watch: {
        // $route(){
        //     if(!this.$store.getters.status){
        //         this.$router.push('/login/')
        //     }
        // },
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
</style>