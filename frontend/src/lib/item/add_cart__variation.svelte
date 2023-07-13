<script>
	import { module, user } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Form from '$lib/module/form.svelte';
	import Button from '$lib/button.svelte';
	import Quantity from '$lib/quantity.svelte';

	let { item } = $module;
	let { variations } = item;

	let error = {};
	let variation = {};
	let quantity = 1;

	const proc = (v) => v.split(':');

	// const init = () => {
	// 	let temp = {};
	// 	for (let i in variation) {
	// 		if (variation[i].length == 1) {
	// 			temp[i] = variation[i][0];
	// 		} else {
	// 			temp[i] = '';
	// 		}
	// 	}

	// 	return temp;
	// };

	const validate = () => {
		error = {};

		let keys = Object.keys(variations);
		for (let i in keys) {
			if (!variation[keys[i]]) {
				error[keys[i]] = `Please select a ${keys[i]}`;
			}
		}
		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/cart`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({
				key: item.key,
				quantity,
				variation,
				ops: 'add'
			})
		});

		resp = await resp.json();

		if (resp.status == 200) {
			$user = resp.user;
			$module = '';
		} else if (resp.error) {
			error.error = resp.error;
		} else {
			error = resp.error;
		}
	};
</script>

<!-- {#if Object.keys(variations).length > 0} -->
<Form>
	<svelte:fragment slot="title">
		<div class="title">Select variation</div>
	</svelte:fragment>

	<section>
		<!-- {#if error.erroe}
				<p class="error">
					{error.erroe}
				</p>
			{/if} -->

		{#each Object.entries(variations) as [key, values]}
			{#if values.length > 1}
				<div class="property">
					<span>{key}</span>

					<div class="value_row">
						{#each values as value}
							{#if key == 'size'}
								<button
									class="size"
									class:active={variation[key] == value}
									on:click={() => {
										variation[key] = value;
									}}
								>
									{value}
								</button>
							{:else}
								<button
									class="value"
									style:background-color={value}
									class:active={variation[key] == value}
									on:click={() => {
										variation[key] = value;
									}}
								>
									{proc(value)[0]}
								</button>
							{/if}
						{/each}
					</div>

					{#if error[key]}
						<p class="error">
							{error[key]}
						</p>
					{/if}
				</div>
			{/if}
		{/each}

		<div class="property">
			<span> quantity </span>
			<Quantity
				quantity={1}
				on:done={(e) => {
					quantity = e.detail.quantity || 1;
				}}
			/>

			{#if error.quantity}
				<p class="error">
					{error.quantity}
				</p>
			{/if}
		</div>
		<Button
			class="primary"
			icon="cart_add"
			name="Add to cart"
			on:click={() => {
				validate();
			}}
		/>
	</section>
</Form>

<!-- {/if} -->

<style>
	.property,
	section {
		display: flex;
		flex-direction: column;
	}

	section {
		color: var(--ac2);
		background-color: var(--ac4);
		gap: var(--sp2);
	}

	.property {
		gap: var(--sp1);
	}
	span {
		font-weight: 500;
		text-transform: capitalize;
	}

	.value_row {
		display: flex;
		flex-wrap: wrap;
		gap: var(--sp1);
	}

	button {
		--size: 30px;

		all: unset;
		cursor: pointer;
		box-sizing: border-box;

		display: flex;
		justify-content: center;
		align-items: center;

		min-width: var(--size);
		height: var(--size);

		font-size: small;

		padding: 0 var(--sp1);
		border-radius: calc(var(--size) / 2);

		color: var(--light_color);
	}

	.value {
		background-color: var(--ac5);
	}

	.active {
		font-weight: 500;
		outline: 2px solid var(--ac2);
		outline-offset: 2px;
	}

	.size {
		color: var(--midtone);
	}
	.size.active {
		color: var(--cl1);
	}
</style>
