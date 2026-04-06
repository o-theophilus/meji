<script>
	import { Icon } from '$lib/macro';
</script>

<section class="margin center">
	<div class="title">Why buy from Meji</div>
	<br />
	<div class="text">
		Meji is your No. 1 trusted online shopping destination in Nigeria. At Meji, we provide you with
		a seamless shopping experience, offering a wide range of products right at your fingertips.
		Whether you're looking for fashion items for men, women, or children, or searching for other
		essentials, we've got you covered.
	</div>

	<div class="card_area">
		<div class="card">
			<div class="icon">
				<Icon icon="sparkles" size="24" />
			</div>
			<div class="bold">Curated Selection</div>
			Only products that meet our standard make it here
		</div>

		<div class="card">
			<div class="icon">
				<Icon icon="shield-check" size="24" />
			</div>
			<div class="bold">Reliable Quality</div>
			Consistency you can depend on, every time
		</div>

		<div class="card">
			<div class="icon">
				<Icon icon="zap" size="24" />
			</div>
			<div class="bold">Effortless Shopping</div>
			A clean, fast experience from start to finish
		</div>

		<div class="card">
			<div class="icon">
				<Icon icon="lock" size="24" />
			</div>
			<div class="bold">Secure Payments</div>
			Safe, trusted transactions with every purchase
		</div>

		<div class="card">
			<div class="icon">
				<Icon icon="truck" size="24" />
			</div>
			<div class="bold">Fast, Reliable Delivery</div>
			Your order, delivered smoothly and on time
		</div>

		<div class="card">
			<div class="icon">
				<Icon icon="clock" size="24" />
			</div>
			<div class="bold">Always Available</div>
			Shop anytime, with support when you need it
		</div>
	</div>
</section>

<style>
	.margin {
		margin: 160px 0;
	}

	.title {
		font-size: 2rem;
		color: var(--ft1);
		line-height: 120%;
		font-weight: 600;
	}

	.text {
		max-width: 600px;
		margin: auto;
	}

	.bold {
		font-weight: 600;
		font-size: 1.2rem;
		color: var(--ft1);
	}

	.center {
		text-align: center;
	}

	.card_area {
		margin-top: 40px;
		display: grid;
		grid-template-columns: repeat(2, 1fr);
		gap: 8px;

		@media screen and (min-width: 580px) {
			&:not(.two) {
				grid-template-columns: repeat(3, 1fr);
			}
		}

		.card {
			display: flex;
			flex-direction: column;
			align-items: center;
			gap: 16px;

			background-color: var(--bg3);
			padding: 24px 16px;
			border-radius: 8px;

			.icon {
				display: flex;
				justify-content: center;
				align-items: center;
				color: var(--ft2);

				width: 48px;
				aspect-ratio: 1;
				border-radius: 40%;
				background-color: var(--bg1);
			}
		}
	}
</style>
