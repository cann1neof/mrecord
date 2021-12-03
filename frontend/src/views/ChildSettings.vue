<template>
    <div v-if="child">
        <div class="container-transparent mx-auto mb-0 pb-0 d-flex justify-space-between">
            <div>
                <mrd-button :to="`/child/${id}/`" dark > 
                    <v-icon> mdi-chevron-left </v-icon> Назад
                </mrd-button>
            </div>
            <div>
                <h1 class="main-title"> Настройки </h1>
            </div>
            <div>
                <mrd-button @click="confirm" dark color="#D96906" > 
                    Сохранить <v-icon> mdi-chevron-right </v-icon>
                </mrd-button>
            </div>    
        </div>

        <v-card width="50vw" class=" mx-auto mt-12 pa-10" color="#013AAA" dark>
            <p style="text-align: center;" >Настройки аккаунта</p>
            
            <v-row style="text-align: center;">
                <v-col cols=4 >
                    Фамилия
                </v-col>
                <v-col cols=4 >
                    {{ child.last_name }}
                </v-col>
                <v-col cols=3 >
                    <v-text-field 
                    v-model="temp_last_name"
                    dense
                    placeholder="Изменить фамилию"
                    color="#A3B2CD"
                    :rules="nameRule"
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
                    {{ child.first_name }}
                </v-col>
                <v-col cols=3 >
                    <v-text-field 
                    v-model="temp_first_name"
                    dense
                    placeholder="Изменить имя"
                    color="#A3B2CD"
                    :rules="nameRule"
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
                    {{ child.second_name }}
                </v-col>
                <v-col cols=3 >
                    <v-text-field 
                    v-model="temp_second_name"
                    dense
                    placeholder="Изменить отчество"
                    color="#A3B2CD"
                    :rules="nameRule"
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
                    {{ child.insurance_number }}
                </v-col>
                <v-col cols=3 >         
                    <v-text-field 
                        v-model="temp_insurance_number"
                        dense
                        placeholder="Изменить страховой номер"
                        color="#A3B2CD"
                        type="number"
                        :counter="16"
                    >
                    </v-text-field>
                </v-col>
            </v-row>
            
        </v-card>

        <v-card width="50vw" class=" mx-auto mt-12 pa-10" color="#013AAA" dark>
            <p style="text-align: center;" >Настройки заболеваний и противопоказаний</p>
            <illnesses-viewer :instance="child.illnesses" @add="addIllness($event)" @del="deleteIllness($event)" >  </illnesses-viewer>
        </v-card>

        <v-card width="50vw" class=" mx-auto mt-12 pa-10" color="#013AAA" dark>
            <p style="text-align: center;" >Настройки заболеваний и противопоказаний</p>
            <recipes-viewer :inline="true" :instance="child.recipes" @add="addRecipe($event)" @del="deleteRecipe($event)" >  </recipes-viewer>
        </v-card>
    </div>
</template>

<script>
import mrdButton from '../components/mrdButton.vue'
import recipesViewer from '../components/recipesViewer.vue'
import illnessesViewer from '../components/illnessesViewer.vue'

export default {
    props: ['id'],
    components: {
        mrdButton,
        recipesViewer,
        illnessesViewer,
    },
    data : () => ({
        child : {},
        temp_last_name : '',
        temp_first_name : '',
        temp_second_name : '',
        temp_insurance_number : '',
    }),
    methods: {
        async validate(){
            if (!this.$store.getters.status)
                this.$router.push('/login')
            else {
                const url = this.$store.getters.url + 'octopus/' +this.$store.getters.token + '/c/?id=' + this.id
                await this.$axios.get(url)
                .then(res => {
                    this.child = res.data
                    this.child.recipes   = JSON.parse(this.child.recipes) 
                    this.child.illnesses = JSON.parse(this.child.illnesses) 
                    console.log(this.child)
                }).catch(err => {
                    if(err.response.status==401){
                        this.$emit('raise', {errCode: 'CU02', errMessage: 'Авторизируйтесь заново'})                    
                        this.$router.push('/login')
                    }
                })
            }
        },
        async confirm(){
            const newChild = {
                last_name : this.temp_last_name ? this.temp_last_name : this.child.last_name,
                first_name : this.temp_first_name ? this.temp_first_name : this.child.first_name,
                second_name : this.temp_second_name ? this.temp_second_name : this.child.second_name,
                insurance_number : this.temp_insurance_number ? this.temp_insurance_number : this.child.insurance_number,
                illnesses : JSON.stringify(this.child.illnesses),
                recipes :   JSON.stringify(this.child.recipes) 
            }
            const url = this.$store.getters.url + 'editor/child/'
            const token = this.$store.getters.token
            this.$axios.put(url, {id: this.id, token: token, data: newChild } )
            .then(res => {
                if(res.status==200){
                    this.$router.push('/my')
                }
            })
            .catch(err => {
                if(err.response.status == 401){
                    this.$emit('raise', {errCode: 'CV02', errMessage: 'Ошибка авторизации. Авторизируйтесь заново.'})
                }
                if(err.response.status == 422){
                    this.$emit('raise', {errCode: 'CV03', errMessage: 'Вы пытаетесь изменить запись несуществующего ребенка. Обратитесь в службу поддержки для дополнительной информации.'})
                }
                if(err.response.status == 400){
                    this.$emit('raise', {errCode: 'CV04', errMessage: 'Ошибка в формате данных. Попробуйте исправить данные и отправить запрос еще раз.'})
                }
                if(err.response.status == 403){
                    this.$emit('raise', {errCode: 'CV05', errMessage: 'Нет доступа'})
                }
            })
        },
        deleteRecipe(index){
            this.child.recipes.splice(index, 1)
        },
        deleteIllness(index){
            this.child.illnesses.splice(index, 1)
        },

        addRecipe(data){
            this.child.recipes.push(data)
        },
        addIllness(data){
            this.child.illnesses.push(data)
        },
    },
    computed:{
        nameRule(){
            return [
                v => ( v.length > 0 && /[a-zA-Zа-яА-Я]+/.test(v)) || 'Неправильный формат данных',
            ]
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
