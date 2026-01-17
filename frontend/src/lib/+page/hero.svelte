<script>
	import { Button } from '$lib/button';
	import { Icon } from '$lib/macro';
	import Wave from './hero.wave.svelte';
	import Nav from './hero.nav.svelte';
	import Customer from './hero.customer.svelte';
	import Bubble from './hero.bubble.svelte';
</script>

<section>
	<div class="nav">
		<Nav />
	</div>

	<div class="wave">
		<Wave />
	</div>

	<div class="block">
		<div class="copy">
			<span class="title">Shopping made easy</span>
			Whoever said money can't buy happiness basically didn't know where to go shopping.
			<div class="btn">
				<br />
				<Button icon2="arrow-right" href="/shop">Shop Now</Button>
			</div>
		</div>

		<div class="image_area">
			<br />
			<div class="bubble">
				<Bubble />
			</div>

			<div class="customers">
				<Customer />
			</div>

			<img src="/image/hero_image.png" alt="hero" />
			<div class="btn">
				<br />
				<Button icon2="arrow-right" href="/shop">Shop Now</Button>
			</div>
		</div>
	</div>
</section>

<style>
	section {
		--bgc: rgb(70, 70, 78);
		position: relative;
		overflow: hidden;

		background: linear-gradient(var(--bgc) 50%, var(--bg2) 50%);
		box-shadow: inset 0 7px 9px -7px rgba(0, 0, 0, 0.5);
	}

	.nav {
		position: relative;
		z-index: 1;
	}

	.wave {
		display: flex;
		justify-content: center;

		position: absolute;
		bottom: 0;

		width: 100%;
		fill: var(--bgc);
	}

	.block {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		gap: var(--sp3);

		width: min(100%, 1000px);

		margin: auto;
		padding: 28px;
		padding-top: 0;

		position: relative;
	}

	.copy {
		display: flex;
		align-items: center;
		flex-direction: column;
		gap: var(--sp1);

		width: 100%;
		max-width: 300px;

		text-align: center;
		color: var(--ac1);
	}

	.title {
		font-size: large;
		font-weight: 900;

		color: var(--cl1);
	}

	.copy .btn {
		display: none;
	}

	.image_area {
		position: relative;

		display: flex;
		flex-direction: column;
		align-items: center;
	}

	img {
		height: 300px;
	}

	.bubble {
		position: absolute;
		top: 20px;
		right: -20px;
	}

	.customers {
		position: absolute;
		top: 150px;
		left: -20px;
	}

	@media screen and (min-width: 800px) {
		.block {
			flex-direction: unset;
			gap: 0;
		}
		.copy {
			align-items: unset;
			text-align: unset;
		}

		.copy .btn {
			display: unset;
		}

		.image_area .btn {
			display: none;
		}

		img {
			height: 400px;
		}

		.bubble {
			top: 40px;
			right: 10px;
		}

		.customers {
			top: 230px;
			left: 0;
		}
	}
</style>
