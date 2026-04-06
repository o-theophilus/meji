<script>
	import Bubble from './hero.bubble.svelte';
	import Customer from './hero.customer.svelte';
</script>

<section>
	<div class="title">
		Whoever said money can't buy happiness basically didn't know where to go shopping.
	</div>

	<div class="image_area">
		<div class="bubble">
			<Bubble />
		</div>

		<div class="customers">
			<Customer />
		</div>

		<img src="/image/hero_image.png" alt="hero" />
	</div>
</section>

<style>
	section {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		gap: 24px;

		padding: 28px;
		padding-bottom: 0;

		background-color: var(--bg);
		border-radius: 8px;
	}

	.title {
		font-size: 1.8rem;
		font-weight: 800;

		text-align: center;
		color: var(--cl1);
	}

	.image_area {
		position: relative;

		display: flex;
		flex-direction: column;
		align-items: center;

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
	}

	@media screen and (min-width: 800px) {
		section {
			flex-direction: unset;
		}

		.title {
			text-align: left;
		}
	}
</style>
