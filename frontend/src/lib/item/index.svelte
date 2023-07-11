<script>
	import Rating from './rating.svelte';
	import Add_Cart from './add_cart.svelte';
	import Save from './save.svelte';

	export let item = {
		name: '[item name]',
		photos: [],
		feedbacks: [],
		price: 0,
		old_price: 0
	};
	export let view_list = false;

	let rating = 0;
	if (item.feedbacks) {
		for (let i in item.feedbacks) {
			rating += item.feedbacks[i].rating;
		}
		rating /= item.feedbacks.length;
	}
</script>

<section class="item" class:view_list>
	<a href="/{item.alias}">
		<img
			src={`${item.photos[0]}/thumbnail` || ''}
			alt={item.name}
			onerror="this.src='/image/item.png'"
		/>
	</a>

	<div class="details_control">
		<a href="/{item.alias}">
			<div class="details">
				<div class="name">
					{item.name}
				</div>
				<div class="row2">
					<div class="cost">
						<div class="price">
							₦{item.price.toLocaleString()}
						</div>
						{#if item.old_price}
							<div class="old_price">
								₦{item.old_price.toLocaleString()}
								<div class="strike" />
							</div>
						{/if}
					</div>
					{#if item.feedbacks.length > 0}
						<Rating {rating} />
					{/if}
				</div>
			</div>
		</a>

		<div class="control">
			<Add_Cart {item} type="2" />
			<Save {item} type="2" on:unsaved on:done />
		</div>
	</div>
</section>

<style>
	.item {
		display: flex;
		flex-direction: column;

		border-bottom: 2px solid var(--ac5);
		overflow: hidden;

		transition: var(--trans1);
	}
	.item:hover {
		transform: scale(1.02);
		border-color: var(--cl1);
	}
	a {
		text-decoration: none;
		color: var(--ac1);

		height: 100%;
	}

	img {
		width: 100%;
		height: 100%;
		border-radius: var(--brad1);
		aspect-ratio: 1/1;
		background-image: url('/image/item.png');
		background-size: cover;
	}

	.details_control {
		display: flex;
		flex-direction: column;

		width: 100%;
	}

	.details {
		display: flex;
		flex-direction: column;
		gap: var(--sp1);
		padding: var(--sp1);
	}
	.row2 {
		display: flex;
		gap: var(--sp1);
		justify-content: space-between;
		height: 30px;
	}
	.control {
		display: flex;
		width: 100%;
	}

	@media screen and (min-width: 500px) {
		.details {
			padding: var(--sp1) var(--sp2);
		}
	}

	.name {
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
	}
	.cost {
		display: flex;
		flex-wrap: wrap;

		align-items: center;
		gap: var(--sp1);
	}
	.price {
		font-weight: 500;
		color: var(--cl3);
	}

	.old_price {
		font-size: small;
		position: relative;
		color: var(--midtone);
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

	.view_list {
		flex-direction: unset;
		height: 200px;
	}

	.view_list img {
		width: unset;
		height: 100%;
	}

	.view_list .details {
		padding: var(--sp1) var(--sp2);
	}

	.view_list .name {
		white-space: unset;
	}
</style>
