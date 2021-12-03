<template>
    <div>
        <div v-if="items[0]">
            <v-row
                v-for="(item, index) in items"
                :key="index"
            >
                <v-col 
                    cols=6
                    v-if="index % 2 == 0"
                >
                    <v-img 
                        :src="item.src" 
                        width= "400px"
                        height="400px"
                        contain
                        class="mx-auto"
                    ></v-img>
                </v-col>
                <v-col 
                    cols=6
                    class="market-product-info pl-6 mb-3"
                    v-if="index % 2 == 0"
                >
                    <h2>{{item.title}}</h2>
                    <h4>Производитель: {{item.distributor}}</h4>
                    <p>
                        {{item.info}}
                    </p>
                    <mrd-button 
                        @click="addToCart(item)"
                        dark
                    >
                    Добавить в корзину
                    </mrd-button>
                </v-col>    

                <v-col 
                    cols=6
                    class="market-product-info pl-6"
                    v-if="index % 2 == 1"
                >
                    <h2>{{item.title}}</h2>
                    <h4>Производитель: {{item.distributor}}</h4>
                    <p>
                        {{item.info}}
                    </p>
                    <mrd-button 
                        @click="addToCart(item)"
                        dark
                    >
                    Добавить в корзину
                    </mrd-button>
                </v-col>    
                <v-col 
                    cols=6
                    v-if="index % 2 == 1"
                    class="mb-3"
                >
                    <v-img 
                        :src="item.src"
                        width= "400px"
                        height="400px"
                        contain
                        class="mx-auto"
                    ></v-img>
                </v-col>
            </v-row>

            <v-dialog
                width="40vw"
                class="px-3 py-2"
                v-model="addToCartDialog"
                v-if="tempCart"
            >
                <v-card>
                    <v-card-title> Вы собираетесь добавить в корзину: </v-card-title>
                    <v-card-text>
                        <v-row>
                            <v-col cols=4>
                                <v-img 
                                    :src="tempCart.src"
                                    width=100	
                                    height=167
                                    contain
                                    class="mx-auto"
                                ></v-img>
                            </v-col>
                            <v-col cols=6>
                                <h2>{{tempCart.title}}</h2>
                                <h4> Производитель: {{tempCart.distributor}}</h4>
                                <p v-if="tempCart.info">{{tempCart.info.substr(0, 160) + '...'}}</p>
                                <p> {{ getQuantity }} </p>
                                <p>Цена: {{tempCart.price}}&#8381;</p>
                                <v-row>
                                    <v-col cols=4>
                                        <mrd-button
                                            dark
                                            ltl
                                            @click="quantityDown"
                                        > <v-icon>mdi-minus</v-icon> </mrd-button>
                                    </v-col>
                                    <v-col cols=4>
                                        <v-text-field
                                            outlined
                                            v-model="qq"
                                            readonly
                                        ></v-text-field>
                                    </v-col>
                                    <v-col cols=4>
                                        <mrd-button
                                            dark
                                            ltl
                                            @click="qq++"
                                        > <v-icon>mdi-plus</v-icon> </mrd-button>
                                    </v-col>
                                </v-row>
                            </v-col>
                        </v-row>
                        <v-row class="full-width mx-2 my-2">
                            <v-col cols=6 >
                                <v-card
                                    class="hover-selection"
                                    @click="select(2)"
                                    height="100%"
                                    flat
                                    dark
                                >
                                    <v-card-title class="full-width">
                                        <h3 class="text-center" style="width: 100%;"> «Security» </h3>
                                    </v-card-title>
                                    <v-card-text>
                                        Конфигурация «Security» позволит максимально обезопасить персональные данные, хранить на чипе только необходимую информацию. Подойдет для занятых людей, опасающихся за безопасность своих данных.
                                    </v-card-text>
                                </v-card>
                            </v-col>
                            <v-col cols=6 >
                                <v-card
                                    class="hover-selection"
                                    @click="select(1)"
                                    height="100%"
                                    flat
                                    dark
                                >
                                    <v-card-title class="full-width">
                                        <h3 class="text-center" style="width: 100%;"> «Spacious» </h3>
                                    </v-card-title>
                                    <v-card-text>
                                        Конфигурация «Spacious» обладает большей вместимостью, чем «Безопасный» вариант чипа, а значит может вмещать в себя больше информации о пациенте. Подойдет для пожилых людей или для людей с большим списком хронических заболеваний.
                                    </v-card-text>
                                </v-card>
                            </v-col>
                        </v-row>
                        <div style="width: 100%; text-align: center;">
                            <mrd-button
                                big 
                                @click="closeAddToCartDialog()" 
                                dark 
                                :disabled="tempCart.quantity[selected-1] === 'NOPE' || tempCart.quantity[selected-1] <= 0"
                            >
                                Добавить
                            </mrd-button>
                        </div>
                    </v-card-text>
                </v-card>
            </v-dialog>
        </div>
        <v-snackbar
			v-model="snackbar"
			bottom
            right
            color="#fff"
            light     
            :timeout="0"
            multi-line=""
		>   
            <div class="darktext mx-2"> В корзине: {{cartQuantityCounter}}шт.</div>
            <div class="darktext mx-2"> Сумма в корзине {{cartPriceCounter}}&#8381; </div>
			<v-btn
				dark
				text
				@click="showCart"
                class="darktext"   
			>
				Перейти в корзину
			</v-btn>
		</v-snackbar>
    </div>
</template>

<script>
import mrdButton from '../components/mrdButton.vue'

export default {
    components: {
        mrdButton,
    },
    data: () => ({
        snackbar: true,
        items: [],
        addToCartDialog: false,
        dialog: false,
        cart: [],
        tempCart: {
            "model": 0,
            "specification": 0,
            "name": "",
            "distributor": "",
            "info": "",
            "price": 0,
            "selector": "[]",
            "src": "",
            "quantity": ""
        },
        qq: 0,
        selected: {},
    }),
    methods: {
        select(index){
            this.selected = index
        },
        addToCart(item){
            if(item){
                this.tempCart = JSON.parse(JSON.stringify(item))
                this.addToCartDialog = true
                this.qq = 1
                this.selected = {}
            }
        },
        quantityDown(){
            if(this.qq > 1)
                this.qq--
            else if(this.qq == 1){
                this.qq--
                this.addToCartDialog = false
            }
        },
        closeAddToCartDialog(){
            if(this.selected){
                const current = this.cart.find(el => el.model == this.tempCart.model && el.selected == this.selected)
                if(!current){
                    this.cart.push(this.tempCart)
                    this.cart[this.cart.length-1]['quantity'] = this.qq
                    this.cart[this.cart.length-1]['selected'] = this.selected
                }else{
                    current.quantity += this.qq            }
                this.addToCartDialog = false
            }
        },
        showCart(){
            console.log(this.cart)
            this.$store.dispatch('updateCart', this.cart)
            this.cart = []
            this.$router.push('/buy/cart')
        },
        async loadItems(){
            const url = this.$store.getters.url + 'market/'
            await this.$axios.get(url).then(res => {
                for(let each of res.data){
                    const current = this.items.find(el => el.model === each.model)
                    if(!current){
                        this.items.push(each)
                    }else{
                        current.specification = [current.specification, each.specification]
                        current.quantity = [current.quantity, each.quantity]
                    }
                }                
                
                for(let each of this.items){
                    each.src = '/' + each.src
                    each.model = parseInt(each.model)
                }
            })
            .catch( ()=>{
                this.$emit('raise', {errCode: 'SM01', errMessage: 'Ошибка при загрузке данных, попробуйте снова'})
            } )
        }
    },
    computed:{
        getQuantity(){
            if(this.tempCart.quantity[this.selected-1] >= 10){
                return 'Есть в наличии'
            }else if(this.tempCart.quantity[this.selected-1] < 10 && this.tempCart.quantity[this.selected-1] > 0){
                return 'Скоро закончится!'
            }else if(this.tempCart.quantity[this.selected-1] == 0){
                return 'Нет в наличии, но скоро будет!'
            }
            return ' '
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
        cartQuantityCounter(){
            let c = 0
            if(this.cart[0]){
                for(let each of this.cart){
                    c += each.quantity
                    console.log('yay')
                }
                return c || 0
            }
            return 0
        }
    },
    watch: {
        $route(){
            this.loadItems()
            const t = this.$store.getters.cart
            this.cart = t ? t : []
        },
        qq(){
            if(this.qq > this.tempCart.quantity[this.selected-1]){
                this.qq = this.tempCart.quantity[this.selected-1]
            }
        },
    },
    mounted(){
        this.loadItems()
        const t = this.$store.getters.cart
        this.cart = t ? t.map(el=>el) : []
    },

    
}
</script>

<style scoped>
.market-product-info{
    background-color: #f4f4f4;
}
.main-title{
    font-size: 30px;
    color: #404040;
}

.hover-selection{
    background-color: #00000066;
}
.hover-selection:hover{
    background-color: #000000AA;
}

.darktext{
    color:#333;
}
</style>
