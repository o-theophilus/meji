<script>
	import Rating from './rating.svelte';
	import Add_Cart from './add_cart.svelte';
	import Save from './save.svelte';

	export let item;
	export let list = false;
</script>

<section class="item" class:list>
	<a data-sveltekit-preload-data="off" class="img" href="/{item.slug}">
		<img
			src={item.photos.length > 0 ? `${item.photos[0]}/200` : '/image/item.png'}
			alt={item.name}
			onerror="this.src='/image/item.png'"
		/>
	</a>

	<div class="details_control">
		<a data-sveltekit-preload-data="off" href="/{item.slug}">
			<div class="details">
				<div class="name">
					{item.name}
				</div>

				<div class="cost">
					<div class="price">
						{#if item.price}
							₦{item.price.toLocaleString()}
						{:else}
							Nil
						{/if}
					</div>
					{#if item.old_price}
						<div class="old_price">
							₦{item.old_price.toLocaleString()}
							<div class="strike" />
						</div>
					{/if}
				</div>
			</div>
		</a>

		<div class="control">
			<Add_Cart {item} type="2" />
			<Save {item} type="2" on:save_start on:save_end />
			<Rating ratings={item.ratings} href="/{item.slug}/feedback" />
		</div>
	</div>
</section>

<style>
	.item {
		display: flex;
		flex-direction: column;

		background-color: var(--ac6);
		border-radius: var(--sp1);
		outline: 2px solid transparent;

		overflow: hidden;
		cursor: pointer;
		transition: var(--trans1);

		box-shadow: var(--shad1);
	}
	.item:hover {
		outline-color: var(--ac1);
	}
	a {
		text-decoration: none;
		color: var(--ac1);
	}

	.img {
		font-size: 0;
	}

	img {
		width: 100%;
		aspect-ratio: 1/1;
		background-image: url('/image/item.png');
		background-size: cover;
	}

	.details_control {
		display: flex;
		flex-direction: column;
		justify-content: space-between;

		width: 100%;
		height: 100%;
	}

	.details {
		padding: var(--sp1) var(--sp2);
	}

	.control {
		display: flex;
		width: 100%;
	}

	.cost {
		display: flex;
		flex-wrap: wrap;

		align-items: center;
		gap: 0 var(--sp1);
	}
	.price {
		font-weight: 500;
		font-size: large;
	}

	.old_price {
		font-size: small;
		position: relative;
		color: var(--ac3);
	}
	.strike {
		position: absolute;
		top: calc(50% - 0.5px);
		left: -3px;
		right: -3px;

		height: 1px;

		transform: rotate(-10deg);
		background: var(--cl4);
	}

	.list {
		flex-direction: unset;
	}

	.list img {
		width: unset;
		height: 120px;
	}

	.list .details {
		padding: var(--sp2);
	}
	.list .details_control {
		height: unset;
	}

	.list .name {
		white-space: unset;
	}
</style>
