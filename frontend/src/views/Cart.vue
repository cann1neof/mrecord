<template>
    <div>
        <v-card
            width = "60vw"
            class="mx-auto my-3"
        >
            <v-card-title
                class="text-center"
            >
                <h2 style="width:100%" >Корзина</h2>
            </v-card-title>
            <v-card-text>
                <v-row v-for="(item, index) in cart" :key="index">
                    <v-col cols=4>
                        <v-img 
                            :src="item.src"
                            width=100	
                            height=167
                            contain
                            class="mx-auto"
                        ></v-img>
                    </v-col>
                    <v-col cols=6>
                        <h2>{{item.title}} <span class="selector-title"> {{item.selector ? JSON.parse(item.selector)[item.selected-1].text : ''}} </span></h2>
                        <h4> Производитель: {{item.distributor}}</h4>
                        <p v-if="item.info">{{item.info.substr(0, 160) + '...'}}</p>
                        <h4>Количество: {{item.quantity}}</h4>                        
                        <mrd-button 
                            @click="deleteItem(index)" 
                            dark 
                            color="#D96906"
                            class="my-3"
                        >
                        Удалить
                        </mrd-button>
                    </v-col>
                </v-row>
                Сумма заказа: {{cartPriceCounter}}&#8381;
            </v-card-text>
        </v-card>

        <v-card 
            width="60vw"
            class="mx-auto my-3"
            v-if="(cart !== null && cart.length > 0) "
        >
            <v-card-title
                class="text-center"
            >
               <h2 style="width:100%" > Оформление заказа </h2>
            </v-card-title>
            <v-card-text>
                <div style="width: 50%" class="mx-auto">
                    <v-form
                        ref="firstInfo"
                    >
                        <v-text-field
                            required
                            v-model="name"
                            outlined
                            placeholder="ФИО"   
                            :rules="nameRules"
                        ></v-text-field>
                        <v-text-field
                            required
                            v-model="email"
                            outlined
                            placeholder="e-mail"   
                            :rules="emailRules"
                        ></v-text-field>
                        <v-select
                            outlined
                            :items="[{value:1, text: 'Самовывоз'}, {value:2, text: 'Курьерская доставка'}]"
                            v-model="selector"
                            placeholder="Способ доставки"
                            required
                        ></v-select>

                        <VuePhoneNumberInput
                            required
                            @update="updatePhone" 
                            v-model="p" 
                            :translations="translations"
                        />
                    </v-form>
                </div>
                <div v-if="selector == 1" style="width: 95%; height: 50vh;" class="mx-auto mt-7">
                    {{mapErrorMessage}}
                    <yandex-map
                        :zoom="10"
                        :coords="[55.74954, 37.621587]"
                        map-type="map"
                        :settings="mapSettings"
                        style="width: 100%; height: 100%;"
                        :controls="['zoomControl']"
                    >
                        <ymap-marker
                            v-for="(item, index) of markers"
                            marker-type="Placemark"
                            :key="index"
                            :coords="item.coords"
                            :marker-id="index"
                            @click="showMarker(index)"
                        >

                        </ymap-marker>
                    </yandex-map>
                </div>

                <div
                    v-if="selector == 2"
                    style="width: 50%" class="mx-auto mt-7"
                >
                <v-form
                    ref="secondInfo"
                >
                    <v-text-field
                        required
                        v-model="address.city"
                        outlined 
                        placeholder="Город"
                        :rules="cityRules"
                    ></v-text-field>
                    <v-row>
                        <v-col cols=6>
                            <v-text-field
                                required
                                v-model="address.street"
                                outlined 
                                placeholder="Улица"
                                :rules="streetRules"
                            ></v-text-field>  
                        </v-col>
                        <v-col cols=3>
                            <v-text-field
                                required
                                v-model="address.building"
                                outlined 
                                messages="Номер дома"
                                :rules="buildingRules"
                                type="number"
                            ></v-text-field>  
                        </v-col>
                        <v-col cols=3>
                            <v-text-field
                                v-model="address.apparatment"
                                outlined 
                                messages="Номер квартиры"
                                type="number"
                            ></v-text-field>  
                        </v-col>
                        <v-col cols=6>
                            <v-text-field
                                required
                                v-model="address.postcode"
                                outlined 
                                placeholder="Почтовый индекс"
                                :rules="postcodeRules"
                                type="number"
                            ></v-text-field>  
                        </v-col>
                        <v-col cols=6>
                            <v-text-field
                                v-model="address.additional"
                                outlined 
                                placeholder="Корпус, подъезд и тп"
                            ></v-text-field>  
                        </v-col>
                    </v-row>
                </v-form>
                </div>
                <v-card-actions class="d-flex justify-space-around mt-3">
                    <mrd-button
                        dark
                        to="/buy/"
                    >
                    Назад
                    </mrd-button>
                    <mrd-button
                        dark
                        @click="validate"
                    >
                    Подтвердить
                    </mrd-button>
                </v-card-actions>
            </v-card-text>
        </v-card>
        <v-card
            v-else
            width="60vw"
            class="mx-auto my-3"
        >
            <v-card-title
                class="text-center"
            >
               <h2 style="width:100%" > Корзина пуста! </h2>
            </v-card-title>

            <v-card-text
                class="text-center"
            >
                <v-img
                    src="../../public/cart-plus.png"
                    width="256px"
                    height="256px"
                    class="mx-auto"
                ></v-img>
                <h3 style="width:100%">
                    Ваша корзина пуста. Давайте вместе ее наполним!
                </h3>
                <mrd-button class="my-3" color="#D96906" big to="/buy/" dark> Наполнить корзину </mrd-button>
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
        cart: [],
        markers: null,
        selector: -1,
        name: '',
        email: '',
        phone: '',
        address: {
            country: '',
            city: '',
            street: '',
            building: '',
            apparatment: '',
            postcode: '',
            additional: '',
        },
        choosenMarker: null,
        mapErrorMessage: '',
        p: '',
        translations:{
            countrySelectorLabel: 'Код страны',
            countrySelectorError: 'Выберите код страны',
            phoneNumberLabel: 'Введите номер телефона',
            example: 'Например:'
        },
        mapSettings: {
            apiKey: '0743cdc0-0634-4b6f-be02-c546c5add538',
            lang: 'ru_RU',
            coordorder: 'latlong',
            version: '2.1'
        },
    }),
    methods: {
        async getCart(){
            this.cart = await this.$store.getters.cart
        },
        deleteItem(index){
            this.cart.splice(index, 1)
            this.$store.dispatch('updateCart', this.cart)
        },
        updatePhone(payload){
            if(payload.isValid){
                this.phone = payload.nationalNumber
                this.address.country = payload.countryCallingCode
            }
        },
        validate(){
            if(this.$refs.firstInfo.validate() && this.phone && this.address.country){
                let data = {
                    name: this.name,
                    email: this.email,
                    phone: this.phone,
                    delivery_type: this.selector,
                    cart: this.generateCart()
                }
                if(this.selector == 1){
                    if(this.choosenMarker){
                        data['address'] = JSON.stringify(this.choosenMarker)
                    } else {
                        this.mapErrorMessage = 'Выберите пункт самовывоза'
                    }
                }
                if(this.selector == 2){
                    if(this.$refs.secondInfo.validate()){
                        data['address'] = this.address
                    }
                }
                const url = this.$store.getters.url + 'market/createorder/'
                this.$axios.post(url, {order: data}).then(res => {
                    if(res.status == 201){
                        this.$router.push('/')
                    }
                }).catch(err => console.log(err))
            }
        },
        generateCart(){
            let data = []
            for(let each of this.cart){
                data.push({
                    model: each.model,
                    quantity: each.quantity,
                    selected: each.selected
                })
            }
            return JSON.stringify(data)
        },
        getMarkers(){
            const url = this.$store.getters.url + 'markers/delivery/'
            this.$axios.get(url).then(res=>{
                this.markers = res.data
            }).catch( () => {
                this.$emit('raise', {errCode: 'SM01', errMessage: 'Ошибка при загрузке данных карты, попробуйте снова'})
            })
        },
        showMarker(i){
            this.mapErrorMessage = ''
            this.choosenMarker = this.markers[i]
        }
    },
    computed:{
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
                v => !!v && this.selector == 2 || 'Необходимо ввести город назначения'
            ]
        },
        streetRules(){
            return [
                v => !!v && this.selector == 2 || 'Необходимо ввести улицу'
            ]
        },
        buildingRules(){
            return [
                v => !!v && this.selector == 2 || 'Необходимо ввести номер дома'
            ]
        },
        postcodeRules(){
            return [
                v => !!v && this.selector == 2 || 'Необходимо ввести почтовый индекс'
            ]
        },
        cartPriceCounter(){
            let c = 0
            if(this.cart[0]){
                for(let each of this.cart){
                    c += each.quantity*each.price
                }
                return c || 0
            }
            return 0
        },
    },
    watch: {
        $route(){
            this.getCart()
        },
        selector(){
            if(this.selector == 1 && !this.markers){
                this.getMarkers()
                
            }
        }
    },
    mounted(){
        this.getCart()
    }
}
</script>

<style scoped>
.selector-title{
    font-size: 18px !important;
    color: #375591 !important;
}
</style>
