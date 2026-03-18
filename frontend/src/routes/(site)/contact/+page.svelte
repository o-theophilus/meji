<script>
	import { Content } from '$lib/layout';
	import { Icon } from '$lib/macro';
	import Form from './form.svelte';
</script>

<Content>
	<div class="page_title">Get In Touch</div>
	<br />
	Got a question or proposal, or just want to say hello? Please go ahead.

	<br />
	<br />
	<br />

	<div class="contact">
		<a href="tel:+2348067397793" class="card">
			<div class="icon">
				<Icon icon="phone"></Icon>
			</div>
			<div class="label">Call</div>
			<div class="value">+234 806 739 7793</div>
		</a>
		<a href="mailto:shop.meji.ng@gmail.com" class="card">
			<div class="icon">
				<Icon icon="mail"></Icon>
			</div>
			<div class="label">Email</div>
			<div class="value">shop.meji.ng&#8203;@gmail.com</div>
		</a>
		<a
			href="https://www.google.com/maps/place/Igando+Bus+Stop/@6.5513295,3.2380606,17z/data=!3m1!4b1!4m5!3m4!1s0x103b8540d0692809:0x4a45a882b29213a8!8m2!3d6.5513242!4d3.2402439"
			target="_blank"
			class="card"
		>
			<div class="icon">
				<Icon icon="map-pin"></Icon>
			</div>
			<div class="label">Location</div>
			<div class="value">Lagos, Nigeria.</div>
		</a>
	</div>

	<div class="area">
		<div class="img"></div>
		<div class="form">
			<Form></Form>
		</div>
	</div>
</Content>

<style>
	.contact {
		display: flex;
		gap: 8px;

		.card {
			display: flex;
			flex-direction: column;
			align-items: center;

			width: 100%;
			background-color: var(--bg3);
			padding: 16px;

			color: var(--ft2);
			text-decoration: none;
			border-radius: 8px;

			transition: background-color 0.2s ease-in-out;

			&:hover {
				background-color: var(--bg2);
			}

			.icon {
				display: flex;
				justify-content: center;
				align-items: center;

				width: 40px;
				aspect-ratio: 1;
				border-radius: 40%;
				background-color: var(--bg2);
			}

			.label {
				margin-top: 8px;
				font-weight: 800;
				font-size: 1.2rem;
				color: var(--ft1);
			}

			.value {
				font-size: 0.8rem;
				text-align: center;
			}
		}
	}

	.area {
		margin-top: 16px;
		display: flex;
		outline: 1px solid var(--ol);
		outline-offset: -1px;
		border-radius: 8px;

		> div {
			width: 100%;
		}

		.img {
			background-color: var(--bg);
		}
		.form {
			background-color: var(--bg);
			padding: 16px;
		}
	}

	@media screen and (min-width: 580px) {
		/* .form_area {
			flex-direction: unset;
		} */
	}
</style>
