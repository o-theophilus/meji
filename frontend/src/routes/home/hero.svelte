<script>
	import Button from '$lib/button.svelte';
	import SVG from './svg.svelte';
	import Nav from './hero.nav.svelte';
</script>

<section>
	<div class="svg">
		<SVG />
	</div>
	<div class="nav">
		<Nav />
	</div>
	<div class="block">
		<div class="first">
			<div class="title">Shopping made easy</div>
			<p class="info">
				Whoever said money can't buy happiness basically didn't know where to go shopping.
			</p>
			<div class="btn">
				<Button name="Shop Now >" class="primary" href="/shop" />
			</div>
		</div>
		<div class="second">
			<div class="bubble">
				<p>
					<span> Offer </span>
					<br />
					20% OFF
				</p>
			</div>
			<div class="customers">
				Valuable Customers
				<div class="customer_img">
					<img src="/image/customers.png" alt="valuavle customers" />
					7k+
				</div>
			</div>
			<img src="/image/hero_image.png" alt="hero" />
			<div class="btn">
				<Button name="Shop Now >" class="primary" href="/shop" />
			</div>
		</div>
	</div>
</section>

<style>
	section {
		/* --primary: var(--ac3); */
		--primary: var(--ac5);
		--secondary: var(--cl3);

		position: relative;

		left: calc(-1 * var(--sp1));
		width: calc(100% + var(--sp1) * 2);

		overflow: hidden;

		background: linear-gradient(var(--primary) 50%, transparent 50%);
		color: var(--ac1);
		box-shadow: inset 0 7px 9px -7px rgba(0, 0, 0, 0.5);
	}
	@media screen and (min-width: 1200px) {
		section {
			width: 100%;
			left: 0;
		}
	}

	.svg {
		fill: var(--primary);
		position: absolute;
		bottom: 0;
		left: -50%;
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

	.first {
		display: flex;
		align-items: center;
		flex-direction: column;
		gap: var(--sp1);
	}

	.info,
	.title {
		text-align: center;
	}
	.title {
		font-size: 2rem;
		font-weight: 600;

		color: var(--cl1);
	}
	.info {
		width: 100%;
		max-width: 300px;
	}
	.first .btn {
		display: none;
	}

	.second {
		position: relative;

		display: flex;
		flex-direction: column;
		align-items: center;

		gap: var(--sp1);
	}

	img {
		height: 300px;
	}

	.bubble {
		--height: 50px;

		position: absolute;
		top: 0;
		right: -20px;

		display: flex;
		justify-content: center;
		align-items: center;

		background-color: var(--secondary);
		width: 100px;
		height: var(--height);

		color: var(--ac5_);

		border-radius: calc(var(--height) / 2);
		font-size: 1.2rem;
		line-height: 14px;
	}
	.bubble::after {
		position: absolute;
		top: calc(100% - 2px);
		left: 20px;

		content: '';
		border: 10px solid var(--secondary);

		border-bottom-color: transparent;
		border-right-color: transparent;
	}

	.bubble span {
		font-size: x-small;
	}

	.customers {
		position: absolute;
		top: 150px;
		left: -20px;

		display: flex;
		flex-direction: column;

		background-color: var(--secondary);
		padding: var(--sp1);

		color: var(--ac5_);

		border-radius: var(--sp0);
		font-size: small;
	}

	.customer_img {
		display: flex;
		gap: var(--sp1);
		align-items: center;
	}
	.customer_img img {
		height: 20px;
	}
	@media screen and (min-width: 800px) {
		.block {
			flex-direction: unset;

			gap: 0;
		}
		.first {
			align-items: unset;
		}

		.info,
		.title {
			text-align: unset;
		}
		.info {
			font-size: 1.2rem;
		}
		.first .btn {
			display: unset;
		}

		.second {
			padding-top: var(--sp3);
		}
		.second .btn {
			display: none;
		}

		img {
			height: 500px;
		}

		.bubble {
			top: 50px;
			right: 50px;
		}

		.customers {
			top: 250px;
			left: 20px;
		}
	}
</style>
