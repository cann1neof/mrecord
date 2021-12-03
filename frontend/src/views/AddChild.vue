<template>
    <div>
        <div class="container-transparent mx-auto mb-0 pb-0 d-flex justify-space-between">
            <div>
                <mrd-button to='/my/settings/' dark > 
                    <v-icon> mdi-chevron-left </v-icon> Назад
                </mrd-button>
            </div>
            <div>
                <h1 class="main-title"> Добавить ребенка </h1>
            </div>
            <div>
                <mrd-button @click="create()" dark color="#D96906" > 
                    Сохранить <v-icon> mdi-chevron-right </v-icon>
                </mrd-button>
            </div>
        </div>

        <v-card width="50vw" class=" mx-auto mt-12 pa-10" color="#013AAA" dark>
            <v-row style="text-align: center;">
                <v-col cols=4 >
                    Фамилия
                </v-col>
                <v-col cols=4 > </v-col>
                <v-col cols=3 >
                    <v-text-field 
                    v-model="last_name"
                    dense
                    hide-details
                    placeholder="Указать фамилию"
                    color="#A3B2CD"
                    >
                    </v-text-field>
                </v-col>
            </v-row>
            
            <v-row style="text-align: center;">
                <v-col cols=4 >
                    Имя
                </v-col>
                <v-col cols=4 > </v-col>
                <v-col cols=3 >
                    <v-text-field 
                    v-model="first_name"
                    dense
                    hide-details
                    placeholder="Указать имя"
                    color="#A3B2CD"
                    >
                    </v-text-field>
                </v-col>
            </v-row>

            <v-row style="text-align: center;">
                <v-col cols=4 >
                    Отчество
                </v-col>
                <v-col cols=4 ></v-col>
                <v-col cols=3 >
                    <v-text-field 
                    v-model="second_name"
                    dense
                    hide-details
                    placeholder="Указать отчество"
                    color="#A3B2CD"
                    >
                    </v-text-field>
                </v-col>
            </v-row>
            
            <v-row style="text-align: center;">
                <v-col cols=4 >
                    Страховой номер
                </v-col>
                <v-col cols=4 > </v-col>
                <v-col cols=3 >         
                    <v-text-field 
                    v-model="insurance_number"
                    dense
                    hide-details
                    placeholder="Указать страховой номер"
                    color="#A3B2CD"
                    >
                    </v-text-field>
                </v-col>
            </v-row>
            <v-row style="text-align: center;">
                <v-col cols=4 >
                    Группа крови
                </v-col>
                <v-col cols=4>
                    <v-select
                        v-model="bloodType"
                        :items="[ '0(I)', 'A(II)', 'B(III)', 'AB(IV)' ]"
                        required
                        label="Группа крови"
                    ></v-select>
                </v-col>
                <v-col cols=4>
                    <v-select
                        v-model="rhesusFactor"
                        :items="[ 'Rh+', 'Rh-' ]"
                        label="Резус фактор"
                        required
                        type="password"
                    ></v-select>
                </v-col>
            </v-row>

            <v-row>
                <v-date-picker
                light
                v-model="birthday"
                required
                reactive
                :landscape="true"
                class="my-3 mx-auto"
                >
                День рождения ребенка
                </v-date-picker>
            </v-row>
            
            <v-checkbox
                v-model="id_exists"
                label="У меня есть жетон MRecord Plus"
            ></v-checkbox>
        </v-card>

        <v-card width="50vw" class=" mx-auto mt-12 pa-10" color="#013AAA" dark v-if="id_exists">       
            <v-form ref="mrdInfo">
                <p>
                    Замечательно, что у Вас есть жетон MRecord Plus! Привяжите его к своей учетной записи.
                </p>
                <v-text-field
                    v-model="serial_number"
                    :counter="6"
                    label="MRecordID"
                    required
                ></v-text-field>

                <v-text-field
                    v-model="code"
                    :counter="8"
                    label="Код подтверждения"
                    required
                ></v-text-field>
            </v-form>
        </v-card>

        <v-card width="50vw" class=" mx-auto mt-12 pa-10" color="#013AAA" dark>
            <p style="text-align: center;" >Настройки заболеваний и противопоказаний</p>
            <illnesses-viewer :instance="illnesses" @add="addIllness($event)" @del="deleteIllness($event)" >  </illnesses-viewer>
        </v-card>

        <v-card width="50vw" class=" mx-auto mt-12 pa-10" color="#013AAA" dark>
            <p style="text-align: center;" >Настройки заболеваний и противопоказаний</p>
            <recipes-viewer :inline="true" :instance="recipes" @add="addRecipe($event)" @del="deleteRecipe($event)" >  </recipes-viewer>
        </v-card>

    </div>
</template>

<script>
import mrdButton from '../components/mrdButton.vue'
import recipesViewer from '../components/recipesViewer.vue'
import illnessesViewer from '../components/illnessesViewer.vue'

export default {
    components: {
        mrdButton,
        recipesViewer,
        illnessesViewer,
    },
    data : () => ({
        id_exists : false,
        last_name: '',
        first_name: '',
        second_name: '',
        insurance_number: '',
        serial_number: '',
        illnesses: [],
        recipes: [],
        bloodType:'',
        rhesusFactor:'',
        birthday : new Date().toISOString().substr(0, 10),
        code : '',
    }),

    methods: {
        async create(){

            const data = {
                'id_exists' : this.id_exists,
                'last_name' : this.last_name,
                'first_name' : this.first_name,
                'second_name' : this.second_name,
                'insurance_number' : this.insurance_number,
                'blood_type' : this.bloodType + ' ' + this.rhesusFactor,
                'birthday' : this.birthday.toString("YYYY-MM-DD"),

                'illnesses' : this.illnesses[0] ? JSON.stringify(this.illnesses) : '[]',
                'recipes'   : this.recipes[0] ? JSON.stringify(this.recipes) : '[]',
            }
            if (this.id_exists){
                data['serial_number'] = this.serial_number
                data['code'] = this.code
            }
            this.$axios.post(this.$store.getters.url + 'creator/c/', {"token": this.$store.getters.token, "data": data})
            .then(res=>{
                if(res.status == 201){
                    this.$router.push('/my')
                }
            }).catch(err=>{
                if(err.response.status == 302){
                    this.$router.push('login')
                }
                if(err.response.status == 400){
                    alert('wrong data')
                }
            })
        },

        async validate(){
            if (!this.$store.getters.status)
                this.$router.push('/login')
        },
        deleteRecipe(index){
            this.recipes.splice(index, 1)
        },
        deleteIllness(index){
            this.illnesses.splice(index, 1)
        },

        addRecipe(data){
            this.recipes.push(data)
        },
        addIllness(data){
            this.illnesses.push(data)
        },

        logOut(){
            this.$store.dispatch('logOut')
            this.$router.push('/login')
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
