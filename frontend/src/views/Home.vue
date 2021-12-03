<template>
	<div class="home">
		<v-row style="padding: 0 2vw;">
			<v-col cols=6>
				<h2 class="mrd-title">
					Что такое MRecord?
				</h2>
				<v-divider color="#333"></v-divider>
				<p class="mrd-text">
					MRecord это электронная картотека – бесплатная система структуризации, анализа и выдачи данных о заболеваниях пользователя. Ваша история болезни будет всегда под рукой. Зачем? Основная идея проекта заключается в оказании оперативной помощи людям, которым она в любой момент может понадобится – от астматиков до эпилептиков. 
					<br /> <br />Для этого был разработан специальный чип MRecord+ . Он может быть установлен в любой аксессуар – браслет, кольцо, жетон. В самом чипе будет встроенная NFC с набором инструкций по первой помощи и основной информацией о пациенте. Получить эту информацию можно через приложение используя NFC-ридер, или просто введя написанный на чипе номер. 

				</p>
			</v-col>
			<v-col cols=6>
				<v-img 
					src="../../public/mrd-chip-logo-small.png" 
					width=300	
					height=400
					class="mx-auto"
					contain
				></v-img>
			</v-col>
		</v-row>

		<background> 
			<v-row>
				<v-col cols=6>
					<v-img 
						src="../../public/mrd-nfc-logo.png" 
						width=390
						height=390
						class="mx-auto"
					></v-img>
				</v-col>
				<v-col cols=6>
					<h2 class="mrd-title">
						Как устроен этот чип?
					</h2>
					<p class="mrd-text">
						NFC - Near Field Connection, связь ближнего действия - технология уже давно используемая в разных сферах жизни. От банков до ключей от Tesla Model 3 - везде пригодилась связь ближнего действия. Эта технология абсолютно безопасна для человека, а ее основой "недостаток" (информация передается только на коротких расстояних, до 10 см) сыграло всем на пользу - это свойство позволяет держать информацию на чипе в безопасности!
						<br> <br> Поднесите смартфон, оснащенный технологией NFC, к нашему чипу MRecord+ и вы сразу получите инструкции, чтобы оказать квалифицированную медицинскую помощь, или изменить данные на своем чипе!
					</p>
				</v-col>
			</v-row>
		</background>

		<div class="mrd-content-center mt-5">			
			<div class="mt-3 mrd-centered-text-7" >
				<p class="mrd-text">
					Но не только этим хороша наша система. Если пользователь наблюдается в одной из больниц-партнеров (не важно – амбулаторно или стационарно), то у него будет возможность автоматически сохранять информацию о приемах в системе. Врачи больниц-партнеров во время приема смогут получать указанную пользователем информацию (например, историю болезни). Также в системе присутствует несколько приятных мелочей. Во-первых, анализ заболеваемости. Он позволит пациенту тщательней следить за своим здоровьем, а врачу – быстрее диагностировать заболевания. Во-вторых, используемое в чипах NFC позволит получать доступ к данным из любой точки мира. В-третьих, использование MRecord - хорошее обоснование для получения страховки на более выгодных условиях, что, несомненно, будет полезно людям с хроническими заболеваниями. 
					<br><br>Наша система будет полезна и рядовому гражданину даже если он не имеет хронических заболеваний и не наблюдается в больницах-партнерах. В приложении и на сайте проекта будет размещаться образовательная информация: как оказывать первую помощь, что нужно делать для профилактики различных заболеваний и еще много разных полезных данных. Эти ликбезы помогут спасти множество жизней. 

				</p>
			</div>

			<mrd-button class="mt-3" to="/register/" big dark color="#D96906"> Присоединиться </mrd-button>
		</div>


		<v-snackbar
			v-model="snackbar"
			bottom=""
		>
			Скачать приложение MRecord
			<v-btn
				dark
				text
				@click="download()"
			>
				Скачать
			</v-btn>
			<v-btn
				dark
				text
				@click="snackbar = false"
			>
				Закрыть
			</v-btn>
		</v-snackbar>
	</div>
</template>

<script>
import mrdButton from '../components/mrdButton.vue'
import Background from '../components/Background.vue'

export default {
	components : {
		Background,
		mrdButton,
	},
	data : () => ({
		snackbar: true,
	}),
	methods:{
		download(){
		this.$axios.get('/static/download/lastest/mrecord.apk', { responseType: 'blob' })
			.then(response => {
				const blob = new Blob([response.data], { type: 'application/vnd.android.package-archive' })
				const link = document.createElement('a')
				link.href = URL.createObjectURL(blob)
				link.download = 'mrecord.apk'
				link.click()
				URL.revokeObjectURL(link.href)
			}).catch(console.error)
		}
	}
}
</script>

<style>
.mrd-text{
	font-size: 18px;
}
.mrd-content-center{
	text-align: center;
}
.mrd-centered-text-7{
	position: relative;
	width: 60vw;
	left: 50%;
	margin-left: -30vw;
}
</style>