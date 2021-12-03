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
                        <h3>{{ each.address.address.region }}, {{ each.address.address.country }}, {{ each.address.address.city }}, {{ each.address.address.street }}, {{ each.address.address.geo_data }} </h3>
                        <p class="mb-1" > <span class="title"> Название: </span> {{ each.address.name }} {{ each.address.additional != "" ? `, ${each.address.additional}` : ''}} </p>
                        <p class="mb-1" > <span class="title"> Дата посещения: </span> {{ each.date }}</p>
                        <p class="mb-1" > <span class="title"> Вел прием: </span> {{ each.doctor }}</p>
                        <p class="mb-1" > <span class="title"> Результат: </span> {{ each.result }}</p>
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
            <v-form ref="hospitalsForm">
                <v-text-field
                    v-model="address"
                    required
                    label="Адресс приема"
                >
                </v-text-field>

                <v-date-picker
                    light
                    v-model="date"
                    reactive
                    :landscape="landscape"
                    class="my-3 mx-3"
                    >
                    Дата приема
                </v-date-picker>

                <v-text-field
                    v-model="doctor"
                    required
                    label="ФИО доктора"
                >
                </v-text-field>

                <v-text-field
                    v-model="result"
                    required
                    label="Результат приема"
                >
                </v-text-field>
                
                <div>
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
        inputer : {
            type : Boolean,
            required : false,
            default : true,
        },
        landscape : {
            type : Boolean,
            required : false,
            default : false,
        },
    },
    data : ()=>({
        address : '',
        date : '',
        doctor : '',
        result : '',
    }),
    methods : {
        add(){
            this.$emit('add', {
                'address' : this.address,
                'date' : this.date,
                'doctor' : this.doctor,
                'result' : this.result,
            })
            this.$refs.contactsForm.reset()

        },
        del(index){
            this.$emit('del', index)
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