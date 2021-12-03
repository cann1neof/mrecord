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
                    <v-col cols=9>
                        <h3> <span class="title"> Название: </span> {{ each.name }} </h3>
                        <p class="mb-1" > <span class="title"> От заболевания: </span>{{ each.code }} | {{ each.info }}  </p>
                        <p class="mb-1" > <span class="title"> Дата назначения: </span> {{ each.start_date }} </p> 
                        <p class="mb-1"  v-if="each.end_date != false" > <span class="title"> Дата окончания курса: </span>{{ each.end_date }} </p>
                    </v-col>

                    <v-col cols=3 v-if="inputer">
                        <mrd-button @click="del(index)">
                            Удалить
                        </mrd-button>
                    </v-col>
                </v-row>            
            </div>
        </div>
        <div class="inputer" v-if="inputer">
            <v-form ref="recipiesForm">
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

                    <v-col cols=6 >
                        <v-text-field
                        v-model="name"
                        required
                        label="Название препарата"
                        >
                        </v-text-field>
                    </v-col>

                </v-row>
                
                <v-checkbox 
                    v-model="withDate"
                    label="Курс препарата имеет дату окончания"
                ></v-checkbox>

                <v-date-picker
                light
                v-model="startDate"
                required
                reactive
                :landscape="landscape"
                class="my-3 mx-3"
                locale="Ru"
                >
                Дата назначения препарата
                </v-date-picker>
                
                <v-date-picker
                light
                v-model="endDate"
                reactive
                :landscape="landscape"
                class="my-3 mx-3"
                v-if="withDate"
                locale="Ru"
                >
                Дата окончания курса препарата
                </v-date-picker>
                <div class="mx-auto" >
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
        inline : {
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
        name : '',
        deseaseCode : '',
        startDate : '', //new Date().toISOString().substr(0, 10),
        endDate : '',
        withDate : false,
        codeValid : true,
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
                if (this.endDate == ''){
                    this.$emit('add', {
                        'name' : this.name,
                        'info' : deseaseName,
                        'code' : this.deseaseCode,
                        'start_date' : this.startDate,
                        'end_date' : false
                    })
                }
                else if (this.codeValid) {
                    this.$emit('add', {
                        'name' : this.name,
                        'info' : deseaseName,
                        'code' : this.deseaseCode,
                        'start_date' : this.startDate,
                        'end_date' : this.endDate,
                    })
                }
                this.$refs.recipiesForm.reset()
            }
        },
        del(index){
            this.$emit('del', index)
        },
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

.inline{
    display: inline-block;
}

</style>