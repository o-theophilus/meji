<script>
	import Quantity from '$lib/comp/quantity.svelte';
	import Value from '$lib/comp/variation_value.svelte';

	export let item;

	const proc = (v) => v.split(':');

	let color = '';
	if (item.variation.color) {
		color = item.variation.color;
	}
	if (item.variation.type) {
		let _c = proc(item.variation.type)[1];
		if (_c) {
			color = _c;
		}
	}
</script>

<section>
	<div class="img">
		<img src={item.photos.length > 0 ? item.photos[0] : '/image/item.png'} alt={item.name} />
	</div>
	<div class="details">
		<div class="h name">
			<a href="/{item.alias}">
				{item.name}
			</a>
			<Value variation={item.variation} />
		</div>

		<div class="h extreme">
			<div class="h">
				<span class="price">
					₦{item.price.toLocaleString()}
				</span>
				<Quantity quantity={item.quantity} on:mod on:del />
			</div>
			₦{(item.price * item.quantity).toLocaleString()}
		</div>
	</div>
</section>

<style>
	section {
		position: relative;

		display: flex;
		gap: var(--gap2);
		align-items: center;
	}
	section:not(:last-child) {
		border-bottom: solid 2px var(--background);
		padding-bottom: var(--gap2);
	}

	.img,
	img {
		height: 100px;
		width: 100px;
		object-fit: cover;
	}
	.details {
		display: flex;
		flex-direction: column;
		gap: var(--gap1);
		width: 100%;
	}
	a {
		text-decoration: none;
		color: var(--font1);
	}

	.name {
		gap: var(--gap1);
	}

	.extreme {
		justify-content: space-between;
	}

	.price {
		color: var(--color3);
	}
</style>
