<script>
	import { module, user } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Form from '$lib/module/form.svelte';
	import Button from '$lib/comp/button.svelte';
	import Quantity from '$lib/comp/quantity.svelte';

	const init = () => {
		let temp = {};
		for (let i in variation_options) {
			if (variation_options[i].length == 1) {
				temp[i] = variation_options[i][0];
			} else {
				temp[i] = '';
			}
		}

		return temp;
	};

	const validate = () => {
		error = {};

		let keys = Object.keys(variation);
		for (let i in keys) {
			if (!variation[keys[i]]) {
				error[keys[i]] = `Please select a ${keys[i]}`;
			}
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		const _resp = await fetch(`${import.meta.env.VITE_BACKEND}cart/${item.key}`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({
				variation,
				quantity,
				operation: 'add'
			})
		});

		if (_resp.ok) {
			let resp = await _resp.json();

			if (resp.status == 200) {
				$user = resp.data.user;
				$module = '';
			} else {
				error = resp.message;
			}
		}
	};

	export let item = {};
	export let variation_options = [];
	let quantity = 1;
	let error = {};
	const proc = (v) => v.split(':');
	let variation = init();
</script>

{#if Object.keys(variation).length == Object.keys(variation_options).length}
	<Form>
		<svelte:fragment slot="title">
			<div class="title">Select variation</div>
		</svelte:fragment>

		<section>
			{#if error.message}
				<p class="error">
					{error.message}
				</p>
			{/if}

			{#each Object.entries(variation_options) as [key, values]}
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
										style:background-color={proc(value)[1]}
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
					on:mod={(e) => {
						quantity = e.detail;
					}}
					on:del={() => {
						quantity = 1;
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
{/if}

<style>
	.property,
	section {
		display: flex;
		flex-direction: column;
	}

	section {
		color: var(--font2);
		background-color: var(--foreground);
		gap: var(--gap2);
	}

	.property {
		gap: var(--gap1);
	}
	span {
		font-weight: 500;
		text-transform: capitalize;
	}

	.value_row {
		display: flex;
		flex-wrap: wrap;
		gap: var(--gap1);
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

		padding: 0 var(--gap1);
		border-radius: calc(var(--size) / 2);

		color: var(--light_color);
	}

	.value {
		background-color: var(--background);
	}

	.active {
		font-weight: 500;
		outline: 2px solid var(--font2);
		outline-offset: 2px;
	}

	.size {
		color: var(--midtone);
	}
	.size.active {
		color: var(--color1);
	}
</style>
