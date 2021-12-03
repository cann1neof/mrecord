<template>
    <div>
        <v-card 
            width="40vw" 
            class=" mx-auto mt-12 pa-10" 
            color="#013AAA" 
            dark
        >
            <v-card-title>
                Заполните форму и с Вами обязательно свяжутся!
            </v-card-title>
            <v-card-text>
                <v-form
                    ref="newPartnerForm"
                >   

                    {{error}}
                   <v-text-field
                        required
                        v-model="companyName"
                        outlined 
                        placeholder="Название компании"
                        :rules="companyRules"
                    ></v-text-field>
                    <v-text-field
                        required
                        v-model="partnerName"
                        outlined 
                        placeholder="ФИО"
                        :rules="nameRules"
                    ></v-text-field>
                    <v-text-field
                        required
                        v-model="email"
                        outlined 
                        placeholder="E-mail"
                        :rules="emailRules"
                    ></v-text-field>
                    <VuePhoneNumberInput
                        required
                        @update="updatePhone" 
                        v-model="p" 
                        :translations="translations"
                        dark
                        dark-color="#013AAA"
                    />
                    {{phoneRules}}
                    <!-- Address -->
                    <v-text-field
                        required
                        v-model="companyAddress.city"
                        outlined 
                        placeholder="Город"
                        class="mt-6"
                        :rules="cityRules"
                    ></v-text-field>
                    <v-row>
                        <v-col cols=6>
                            <v-text-field
                                required
                                v-model="companyAddress.street"
                                outlined 
                                placeholder="Улица"
                                :rules="streetRules"
                            ></v-text-field>  
                        </v-col>
                        <v-col cols=3>
                            <v-text-field
                                required
                                v-model="companyAddress.building"
                                outlined 
                                messages="Номер дома"
                                :rules="buildingRules"
                                type="number"
                            ></v-text-field>  
                        </v-col>
                        <v-col cols=6>
                            <v-text-field
                                required
                                v-model="companyAddress.postcode"
                                outlined 
                                placeholder="Почтовый индекс"
                                :rules="postcodeRules"
                                type="number"                        
                            ></v-text-field>  
                        </v-col>
                        <v-col cols=6>
                            <v-text-field
                                v-model="companyAddress.additional"
                                outlined 
                                placeholder="Корпус, подъезд и тп"
                            ></v-text-field>  
                        </v-col>
                    </v-row>
                    <div 
                        style="width: 100%;" 
                        class="text-center"
                    >
                        <mrd-button
                            dark
                            @click="validate"
                            color="#D96906"
                        >
                        Подвердить
                        </mrd-button>
                    </div>
                </v-form>
            </v-card-text>
        </v-card>
    </div>
</template>

<script>
import mrdButton from '../components/mrdButton.vue'
import VuePhoneNumberInput from 'vue-phone-number-input';
import 'vue-phone-number-input/dist/vue-phone-number-input.css';

export default {
    components: {
        mrdButton,
        VuePhoneNumberInput,
    },
    data: () => ({
        companyName: '',
        companyAddress: {
            country: '',
            city: '',
            street: '',
            building: '',
            apparatment: '',
            postcode: '',
            additional: '',
        },
        phone: '',
        p: '',
        partnerName: '',
        email: '',
        error: '',
        translations:{
            countrySelectorLabel: 'Код страны',
            countrySelectorError: 'Выберите код страны',
            phoneNumberLabel: 'Введите номер телефона',
            example: 'Например:'
        },
    }), 
    methods: {
        updatePhone(payload){
            if(payload.isValid){
                this.phone = payload.nationalNumber
                this.companyAddress.country = payload.countryCallingCode
            }else{
                this.phone=''
                this.companyAddress.country = ''

            }
        },
        async validate(){
            if(this.$refs.newPartnerForm.validate() && this.phone && this.companyAddress.country){
                const new_partner = {
                    address: JSON.stringify(this.companyAddress),
                    company: this.companyName,
                    phone: this.phone,
                    name: this.partnerName,
                    email: this.email
                }
                const url = this.$store.getters.url + 'newpartner/'
                let answer = null
                try{
                    answer = await this.$axios.post(url, {new_partner})
                }catch(err){
                    if(err.response.status==400){
                        this.error = 'Неправильный формат данных'
                    }
                    else console.log(err.response)
                    return
                }
                if(answer.status == 201){
                    this.$router.push('/map')
                }
            }
        }
    },
    computed: {
        emailRules(){
            return [
                v => !!v || 'Необходимо ввести email',  
                v => /.+@.+\..+/.test(v) || 'Неправильный email',
            ] 
        },
        nameRules(){
            return [
                v => !!v || 'Необходимо ввести ФИО'
            ]
        },
        cityRules(){
            return [
                v => !!v || 'Необходимо ввести город назначения'
            ]
        },
        streetRules(){
            return [
                v => !!v || 'Необходимо ввести улицу'
            ]
        },
        buildingRules(){
            return [
                v => !!v || 'Необходимо ввести номер дома'
            ]
        },
        postcodeRules(){
            return [
                v => !!v || 'Необходимо ввести почтовый индекс'
            ]
        },
        companyRules(){
            return [
                v => !!v || 'Необходимо ввести название компании'
            ]
        },
        phoneRules(){
            return this.phone ? '' : 'Это поле обязательно для заполнения'
        }
    },
}
</script>
