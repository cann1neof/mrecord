<template>
    <div>
        <div class="container-transparent mx-auto mb-0 pb-0 d-flex justify-space-between">
            <div>
                <mrd-button to='/my/' dark > 
                    <v-icon> mdi-chevron-left </v-icon> Назад
                </mrd-button>
            </div>
            <div>
                <h1 class="main-title"> Настройки </h1>
            </div>
            <div>
                <mrd-button @click="dialog=true" dark color="#D96906" > 
                    Сохранить <v-icon> mdi-chevron-right </v-icon>
                </mrd-button>
                
                <v-dialog
                    v-model="dialog"
                    width="30vw"
                    class="px-3 py-2"
                >   
                    <v-card>
                        <v-card-title
                            primary-title
                        >
                        Подтверждение изменений
                        </v-card-title>

                        <p class="mx-12">
                        Введите текущий пароль, чтобы подтвердить измененния
                        </p>

                        <v-text-field
                            v-model="answer"
                            class="mx-12 py-0 mt-0 mb-3"
                            placeholder="Текущий пароль"
                            hide-details
                            type="password"                            
                        ></v-text-field>

                        <v-card-actions>
                            <mrd-button @click="continueEditing()" dark class="mx-auto"> 
                                Подтвердить
                            </mrd-button>
                        </v-card-actions>
                    </v-card>
                </v-dialog>
            </div>
        </div>

        <v-card width="50vw" class=" mx-auto mt-12 pa-10" color="#013AAA" dark>
            <p style="text-align: center;" >Настройки аккаунта</p>
            
            <v-row style="text-align: center;">
                <v-col cols=4 >
                    Фамилия
                </v-col>
                <v-col cols=4 >
                    {{ last_name }}
                </v-col>
                <v-col cols=4 >
                    <v-text-field 
                    outlined
                    v-model="temp_last_name"
                    dense
                    hide-details
                    placeholder="Изменить фамилию"
                    color="#A3B2CD"
                    >
                    </v-text-field>
                </v-col>
            </v-row>
            
            <v-divider class="field-divider" ></v-divider>
            
            <v-row style="text-align: center;">
                <v-col cols=4 >
                    Имя
                </v-col>
                <v-col cols=4 >
                    {{ first_name }}
                </v-col>
                <v-col cols=4 >
                    <v-text-field 
                    outlined
                    v-model="temp_first_name"
                    dense
                    hide-details
                    placeholder="Изменить имя"
                    color="#A3B2CD"
                    >
                    </v-text-field>
                </v-col>
            </v-row>
            
            <v-divider class="field-divider" ></v-divider>

            <v-row style="text-align: center;">
                <v-col cols=4 >
                    Отчество
                </v-col>
                <v-col cols=4 >
                    {{ second_name }}
                </v-col>
                <v-col cols=4 >
                    <v-text-field 
                    outlined
                    v-model="temp_second_name"
                    dense
                    hide-details
                    placeholder="Изменить отчество"
                    color="#A3B2CD"
                    >
                    </v-text-field>
                </v-col>
            </v-row>
            
            <v-divider class="field-divider" ></v-divider>

            <v-row style="text-align: center;">
                <v-col cols=4 >
                    Электронная почта
                </v-col>
                <v-col cols=4 >
                    {{ email }}
                </v-col>
                <v-col cols=4 >
                    <v-text-field 
                    outlined
                    v-model="temp_email"
                    dense
                    hide-details
                    placeholder="Изменить электронную почту"
                    color="#A3B2CD"
                    >
                    </v-text-field>
                </v-col>
            </v-row>

            <v-divider class="field-divider" ></v-divider>

             <v-row style="text-align: center;">
                <v-col cols=4 >
                    Номер телефона
                </v-col>
                <v-col cols=4 >
                    {{ telephone }}
                </v-col>
                <v-col cols=4>
                    <VuePhoneNumberInput
                        required
                        @update="updatePhone" 
                        v-model="p" 
                        :translations="translations"
                        dark
                        dark-color="#013AAA"
                    />
                </v-col>
            </v-row>

            <v-divider class="field-divider" ></v-divider>
            
            <v-row style="text-align: center;">
                <v-col cols=4 >
                    Пароль
                </v-col>
                <v-col cols=4 >
                    ********
                </v-col>
                <v-col cols=4 >
                    <mrd-button 
                        color="#D96906"
                        @click="passwordDialog=true"
                        dark
                    >
                        Сменить пароль
                    </mrd-button>
                </v-col>
            </v-row>
            
            <v-divider class="field-divider" ></v-divider>
            
            <v-row style="text-align: center;">
                <v-col cols=4 >
                    Логин
                </v-col>
                <v-col cols=4 >
                    {{ username }}
                </v-col>
                <v-col cols=4 >
                    <v-text-field 
                    outlined
                    v-model="temp_username"
                    dense
                    hide-details
                    placeholder="Изменить логин"
                    color="#A3B2CD"
                    >
                    </v-text-field>
                </v-col>
            </v-row>
            
            <v-divider class="field-divider" ></v-divider>
            
            <v-row style="text-align: center;">
                <v-col cols=4 >
                    Страховой номер
                </v-col>
                <v-col cols=4 >
                    {{ insurance_number }}
                </v-col>
                <v-col cols=4 >         
                    <v-text-field 
                    outlined
                    v-model="temp_insurance_number"
                    dense
                    hide-details
                    placeholder="Изменить страховой номер"
                    color="#A3B2CD"
                    >
                    </v-text-field>
                </v-col>
            </v-row>
            
            <v-divider class="field-divider" ></v-divider>
            
            <v-row style="text-align: center;">
                <v-col cols=4 >
                    MRecord ID
                </v-col>
                <v-col cols=4 >
                    #{{ serial_number }}
                </v-col>
                <v-col cols=4 >
                    <mrd-button 
                        color="#D96906"
                        @click="mrecordidDialog=true"
                        dark
                    >
                        Сменить MRecord ID
                    </mrd-button>
                </v-col>
            </v-row>
        </v-card>

        <v-card width="50vw" class=" mx-auto mt-12 pa-10" color="#013AAA" dark>
            <p style="text-align: center;" >Настройки заболеваний и противопоказаний</p>
            <illnesses-viewer :instance="illnesses" @add="addIllness($event)" @del="deleteIllness($event)" >  </illnesses-viewer>
        </v-card>

        <v-card width="50vw" class=" mx-auto mt-12 pa-10" color="#013AAA" dark>
            <p style="text-align: center;" >Настройки заболеваний и противопоказаний</p>
            <recipes-viewer :inline="true" :instance="recipes" @add="addRecipe($event)" @del="deleteRecipe($event)" >  </recipes-viewer>
        </v-card>
        <v-card width="50vw" class=" mx-auto mt-12 pa-10" color="#013AAA" dark>
            <p style="text-align: center;" >Настройки контактов</p>
            <contacts-viewer :instance="contacts" @add="addContact($event)" @del="deleteContact($event)" >  </contacts-viewer>
        </v-card>

        <v-card width="50vw" class=" mx-auto mt-12 pa-10" color="#013AAA" dark>
            <p style="text-align: center;" >Настройки родительского доступа</p>
            <div class="mx-auto my-2" style="width:100px">
                <mrd-button color="#D96906"  to="/my/addchild/">
                    Добавить
                </mrd-button>
            </div>

            <children-viewer :inputer="true" :instance="children" @add="addChild($event)" @del="deleteChild = true; current_child = $event" >  </children-viewer>
            <v-dialog
                v-model="deleteChild"
                width="30vw"
                class="px-3 py-2"
            >   
                <v-card>
                    <v-card-title
                        primary-title
                    >
                    Почему вы хотите удалить запись ребенка?
                    </v-card-title>

                    <v-select
                        :items="[{text:'Запись создана по ошибке', value: 1}, {text:'Ребенок уже совершеннолетний', value: 2}, {text:'Смена родителя', value: 3}]"
                        v-model="selectedReason"
                        class="mx-12"
                    >

                    </v-select>

                    <v-card-actions>
                        <mrd-button @click="continueEditingDeleting()" dark class="mx-auto"> 
                            Подтвердить
                        </mrd-button>
                    </v-card-actions>
                </v-card>
            </v-dialog>
        </v-card>
        <div style="width:100px" class="mx-auto mt-4">
            <mrd-button @click="logOut" dark color="#A60000">Выход</mrd-button>
        </div>

        <!-- password dialog -->
        <v-dialog
            v-model="passwordDialog"
            width="30vw"
        >
            <v-card>
                <v-card-title>
                    Смена пароля
                </v-card-title>
                <v-card-subtitle>
                    Чтобы не сменить пароль случайно, повторите его два раза.
                </v-card-subtitle>
                <v-card-text>
                    <v-text-field 
                        outlined
                        type="password"
                        placeholder="Новый пароль"
                        v-model="temp_password"
                    ></v-text-field>

                    <v-text-field 
                        outlined
                        type="password"
                        placeholder="Повторите пароль"
                        v-model="confirmed_password"
                    ></v-text-field>
                </v-card-text>
                <v-card-actions>
                    <mrd-button
                        @click="confirmPassword()"
                        dark
                    >
                        Подтвердить
                    </mrd-button>
                </v-card-actions>
            </v-card>
        </v-dialog>

        <v-dialog
            v-model="mrecordidDialog"
            width="30vw"
        >
            <v-card>
                <v-card-title>
                    Смена MRecord ID
                </v-card-title>
                <v-card-text>
                    <v-text-field
                        outlined
                        v-model="temp_serial_number"
                        placeholder="Новый MRecord ID"
                    ></v-text-field>
                    <v-text-field
                        outlined
                        v-model="temp_code"
                        placeholder="Код подтверждения"
                    ></v-text-field>
                </v-card-text>
                <v-card-actions>
                    <mrd-button
                        @click="mrecordidDialog = !mrecordidDialog"
                        dark
                    >
                        Подтвердить
                    </mrd-button>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </div>
</template>

<script>
import mrdButton from '../components/mrdButton.vue'
import recipesViewer from '../components/recipesViewer.vue'
import illnessesViewer from '../components/illnessesViewer.vue'
import childrenViewer from '../components/childrenViewer.vue'
import contactsViewer from '../components/contactsViewer.vue'
import VuePhoneNumberInput from 'vue-phone-number-input';
import 'vue-phone-number-input/dist/vue-phone-number-input.css';


export default {
    components: {
        mrdButton,
        recipesViewer,
        illnessesViewer,
        childrenViewer,
        contactsViewer,
        VuePhoneNumberInput,
    },
    data : () => ({
        selectedReason : 0,
        deleteChild : false,
        current_child : -1,
        last_name: '',
        first_name: '',
        second_name: '',
        serial_number: '',
        insurance_number: '',
        blood_type: '',
        email: '',
        telephone : '',
        password: '',
        username: '',
        illnesses: [],
        contacts: [],
        hospitals: [],
        recipes: [],
        children: [],
        
        user: {},
        record: {},
        mrd: {},

        temp_last_name: '',
        temp_first_name: '',
        temp_second_name: '',
        temp_serial_number: '',
        temp_insurance_number: '',
        temp_code: '',
        temp_email: '',
        temp_phone : '',
        temp_country: '',
        p: '',
        temp_password: '',
        temp_username: '',
        output_password: '',
        answer: '',
        confirmed_password: '',

        dialog: false,
        mrecordidDialog: false,
        passwordDialog: false,
        translations:{
            countrySelectorLabel: 'Код страны',
            countrySelectorError: 'Выберите код страны',
            phoneNumberLabel: 'Введите номер телефона',
            example: 'Например:'
        },
    }),
    methods: {
        async validate(){
            if (!this.$store.getters.status)
                this.$router.push('/login')
            else {
                const userStore = this.$store.getters.user
                const recordStore = this.$store.getters.record
                
                this.first_name         = userStore.first_name
                this.second_name        = userStore.second_name
                this.last_name          = userStore.last_name
                this.email              = userStore.email
                this.telephone          = userStore.telephone
                this.username           = userStore.username
                this.password           = userStore.password
                this.serial_number      = recordStore.serial_number
                this.insurance_number   = recordStore.insurance_number.toString().substr(0, 4) + ' ' + recordStore.insurance_number.toString().substr(4, 4) + ' ' + recordStore.insurance_number.toString().substr(8, 4) + ' ' + recordStore.insurance_number.toString().substr(12, 4)
                this.blood_type         = recordStore.blood_type
                this.illnesses          = recordStore.illnesses
                this.contacts           = recordStore.contacts
                this.hospitals          = recordStore.hospitals
                this.recipes            = recordStore.recipes
                this.children           = recordStore.children
            }
        },
        async confirmPassword(){   
            if (this.temp_password === this.confirmed_password){
                await this.$axios.get(this.$store.getters.url + 'register/').then( async (res) => {
                    this.user['password'] = this.temp_password
                    this.user['salt'] = res.data.salt
                } )
                this.passwordDialog = false
            }
            else {
                this.temp_password = ''
                this.confirmed_password = ''
            }
        },
        async continueEditing(){
            const sha256 = require('sha256')            
            this.dialog = false; 
            if(sha256( this.answer + this.$store.getters.salt ) == this.$store.getters.password){
                if(this.temp_first_name){
                    this.user['first_name'] = this.temp_first_name
                }
                if(this.temp_second_name){
                    this.user['second_name'] = this.temp_second_name
                }
                if(this.temp_last_name){
                    this.user['last_name'] = this.temp_last_name
                }
                if(this.temp_email){
                    this.user['email'] = this.temp_email
                }
                if (this.temp_serial_number && this.temp_code){
                    this.record['serial_number'] = this.temp_serial_number 
                    this.record['code'] = this.temp_code
                }
                if (this.temp_insurance_number){
                    this.record['insurance_number'] = this.temp_insurance_number

                }
                if(this.temp_username){
                    this.user['username'] = this.temp_username
                }
                if(this.temp_phone){
                    this.user['telephone'] = this.temp_phone
                }
                if(this.temp_country){
                    this.user['country'] = this.temp_country
                }
                
                this.record['illnesses']    = JSON.stringify( this.illnesses )
                this.record['contacts']     = JSON.stringify( this.contacts )
                this.record['hospitals']    = JSON.stringify( this.hospitals )
                this.record['recipes']      = JSON.stringify( this.recipes )
                this.record['children']     = JSON.stringify( this.children )
                
                const usver = this.user
                if(this.temp_password){
                    usver.password = usver.salt + '$' + sha256(usver.password+usver.salt)
                    await this.$store.dispatch('setNewPassword', {salt: usver.salt, password: sha256(usver.password+usver.salt)})
                }

                const serverData = {
                    'token' : this.$store.getters.token,
                    'usr' : usver,
                    'rec' : this.record,
                }
                console.log(serverData)
                await this.$axios.put(this.$store.getters.url + 'editor/', serverData).then(res=>{
                    console.log(res)
                    if(res.status==200){
                        this.$router.push('/my')
                    }
                }).catch(err =>{
                    if(err.response.status==401){
                        this.$router.push('/login')
                    }
                    // if(err.response.status==400){
                    //     if(err.response.data.find('serialNumberError')){
                    //         this.$emit('raise', {errCode: 'CE01', errMessage: 'Неправильный паро'})
                    //     }
                    // }
                    console.log(err.response)
                    this.user = {}
                    this.record = {}

                })       
            }
            else{
                this.$emit('raise', {errCode: 'UE01', errMessage: 'Неправильный пароль'})
            }
        },
        deleteRecipe(index){
            this.recipes.splice(index, 1)
        },
        deleteIllness(index){
            this.illnesses.splice(index, 1)
        },
        deleteContact(index){
            this.contacts.splice(index, 1)
        },

        addRecipe(data){
            this.recipes.push(data)
        },
        addIllness(data){
            this.illnesses.push(data)
        },
        addContact(data){
            this.contacts.push(data)
        },
        addChild(data){
            this.children.push(data)
        },
        logOut(){
            this.$store.dispatch('logOut')
            this.$router.push('/login')
        },
        continueEditingDeleting(){
            if(this.selectedReason === 1){
                this.children.splice(this.current_child, 1)
            }
            if(this.selectedReason === 2){
                const url = this.$store.getters.url + 'startmigrationsession/'
                const serial_number = this.children[this.current_child].serial_number
                this.$axios.post(url, {token: this.$store.getters.token, id: serial_number})
                .then(res => {
                    if(res.status == 200){
                        this.$store.dispatch('setMigrationToken', res.data.token)
                        this.$router.push('/child/' + serial_number + '/migrate')
                    }
                }).catch(err => {
                    if(err.response.status == 401){
                        this.$router.push('/login')
                    }
                    
                })
            }

            this.deleteChild = false
        },
        updatePhone(payload){
            if(payload.isValid){
                this.temp_phone = payload.nationalNumber
                this.temp_country = payload.countryCallingCode
            }
        },
    },
    watch: {
        $route(){
            this.validate()
        },
    },
    mounted(){
        this.validate()
    }
}
</script>

<style scoped>
.container{
    background-color: #A3B2CD;
    padding: 20px 15px;
    margin-bottom: 12px;
    box-sizing: border-box;
    color: #505050;
    font-weight: bold;
    border-radius: 7px;
    width: 50vw;
}

.container-transparent{
    background-color: transparent;
    padding: 20px 15px;
    margin-bottom: 12px;
    box-sizing: border-box;
    color: #505050;
    font-weight: bold;
    border-radius: 7px;
    width: 50vw;
}
.cont-title{
    font-size: 14px;
    font-weight: lighter;
}
.block-title{
    font-weight: bolder;
    color: #505050;
}

.field-divider{
    margin: 0 auto;
    width: 70%;
}

.main-title{
    font-size: 37px;
    color: #404040;
}
</style>
