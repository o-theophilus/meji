<script>
	import { Content, PageTitle } from '$lib/layout';
	import { Icon, Log, Meta } from '$lib/macro';
	import Form from './form.svelte';
</script>

<Log entity_type={'page'} />
<Meta
	title="Contact Us"
	description="Get support for your orders, payments, and inquiries — fast, simple, and reliable."
/>

<Content>
	<PageTitle>
		{#snippet title()}
			How Can We Help You Today?
		{/snippet}
		{#snippet copy()}
			Get support for your orders, payments, and inquiries — fast, simple, and reliable.
		{/snippet}
	</PageTitle>

	<div class="contact">
		<a href="tel:+2347077033699" class="card">
			<div class="icon">
				<Icon icon="phone" size="24"></Icon>
			</div>
			<div class="label">Call</div>
			<div class="value">+234 707 703 3699</div>
		</a>
		<a href="mailto:admin@meji.ng" class="card">
			<div class="icon">
				<Icon icon="mail" size="24"></Icon>
			</div>
			<div class="label">Email</div>
			<div class="value">admin@meji.ng</div>
		</a>

		<a href="https://wa.me/2347077033699?text=Hello Meji" target="_blank" class="card">
			<div class="icon">
				<Icon icon="whatsapp" size="24"></Icon>
			</div>
			<div class="label">Chat</div>
			<div class="value">WHatsapp</div>
		</a>
	</div>

	<div class="contact">
		<a
			href="https://www.google.com/maps/place/Igando+Bus+Stop/@6.5513295,3.2380606,17z/data=!3m1!4b1!4m5!3m4!1s0x103b8540d0692809:0x4a45a882b29213a8!8m2!3d6.5513242!4d3.2402439"
			target="_blank"
			class="card"
		>
			<div class="icon">
				<Icon icon="map-pin" size="24"></Icon>
			</div>
			<div class="label">Location</div>
			<div class="value">Lagos, Nigeria.</div>
		</a>
		<a href="/faq" class="card">
			<div class="icon">
				<Icon icon="message-circle-question-mark" size="24"></Icon>
			</div>
			<div class="label">FAQ</div>
		</a>
	</div>

	<div class="area">
		<div class="img">
			<img src="/image/contact.jpg" alt="contact us" />
		</div>
		<div class="form">
			<Form></Form>
		</div>
	</div>
</Content>

<style>
	.contact {
		display: flex;
		flex-direction: column;
		gap: 8px;

		&:not(:first-of-type) {
			margin-top: 8px;
		}

		@media screen and (min-width: 380px) {
			flex-direction: row;
		}

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
				color: var(--ft2);
				fill: currentColor;

				width: 48px;
				aspect-ratio: 1;
				border-radius: 40%;
				background-color: var(--bg1);
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
		flex-direction: column;

		overflow: hidden;
		border-radius: 8px;
		background-color: var(--bg);

		.form {
			width: 100%;
			padding: 24px;
		}

		.img {
			width: 100%;
			height: 300px;

			img {
				width: 100%;
				height: 100%;
				object-position: top;
				object-fit: cover;
			}
		}

		@media screen and (min-width: 580px) {
			flex-direction: row-reverse;

			.img {
				height: unset;
			}
		}
	}
</style>
