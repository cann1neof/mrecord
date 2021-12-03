<template>
    <div>
        <div 
            class="viewer"
            v-if="instance"
        >
            <div 
                class="viewer-item" 
                v-for="(each, index) in instance" 
                :key="index"
            >
                <v-row>
                    <v-col :cols="colsCounter" >
                        <h3> <span class="title"> Название заболевания: </span> {{ each.info }} </h3>
                        <p class="mb-1" > <span class="title"> Код по МКБ-10: </span> {{ each.code }} </p>
                        <p class="mb-1" > <span class="title"> Дата диагностирования: </span> {{ each.start_date }} </p> 
                    </v-col>

                    <v-col cols=3  v-if="inputer">
                        <mrd-button @click="del(index)"> 
                            Удалить
                        </mrd-button>
                    </v-col>
                </v-row>
            </div>
        </div>
        <div class="inputer" v-if="inputer">
            <v-form ref="deseaseForm">
                <v-row>
                    <v-col cols=6 >
                        <v-text-field
                        v-model="deseaseCode"
                        :counter="4"
                        required
                        label="Код заболевания по МКБ-10"
                        >
                        </v-text-field>
                    </v-col>
                </v-row>
                <v-date-picker
                light
                v-model="startDate"
                required
                reactive
                :landscape="landscape"
                class="my-3 mx-3"
                locale="Ru"
                >
                Дата диагностирования
                </v-date-picker>

                <div class="mx-auto">
                    <mrd-button @click="add()" dark color="#D96906" > 
                        Добавить
                    </mrd-button>
                </div>
            </v-form>
        </div>
    </div>
</template>

<script>
import mrdButton from '../components/mrdButton.vue'

export default {
    components : { mrdButton },
    props:{
        instance : {
            type : Array,
            required : true,
        },
        landscape : {
            type : Boolean,
            required : false,
            default : false,
        },
        inputer : {
            type : Boolean,
            required : false,
            default : true,
        }
    },
    data : ()=>({
        deseaseCode : '',
        startDate : '', //new Date().toISOString().substr(0, 10),
        endDate : '',
        codeValid : false,
    }),
    methods : {
        async add(){
            let deseaseName = ''
            await this.$axios.get( this.$store.getters.url + `disease/${this.deseaseCode}/` )
            .then( res => { 
                if(res.status == 200){
                    deseaseName = res.data.info
                    this.codeValid = true  
                }
            }).catch( err => {
                if(err.response.status == 404){
                    alert('Неправильный код! Убедитесь в правильности написания или исправьте в соответсвии с примером - A000')
                }
                this.codeValid = false
            } )

            if(this.codeValid){
                this.$emit('add', {
                    'info' : deseaseName,
                    'code' : this.deseaseCode,
                    'start_date' : this.startDate,
                })
                this.$refs.deseaseForm.reset()
            }
        },
        del(index){
            this.$emit('del', index)
        },
    },
    computed: {
        colsCounter(){
            if(this.inputer){
                return 9
            }else{
                return 12
            }
        }
    },
}
</script>

<style scoped>
.viewer-item{
    background-color: #A3B2CD;
    padding: 20px 15px;
    margin-bottom: 12px;
    box-sizing: border-box;
    color: #505050;
    font-weight: bold;
    border-radius: 7px;
    width: 100%;
    font-weight: bold;
}
.title{
    font-size: 14px;
    font-weight:300;
}
</style>