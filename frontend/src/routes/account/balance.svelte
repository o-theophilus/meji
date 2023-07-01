<script context="module">
	export async function load({ session }) {
		if (session.user.login) {
			return {
				props: {
					user: session.user
				}
			};
		}

		return {
			status: 302,
			redirect: '/?module=login&return_url=account'
		};
	}
</script>

<script>
	import { user, currency, module } from '$lib/store.js';

	import Card from '$lib/comp/card.svelte';
	import Title from '$lib/comp/card_title.svelte';
	import Body from '$lib/comp/card_body.svelte';
	import Button from '$lib/comp/button.svelte';

	import Add from './_add_voucher.svelte';

	export let user;
	$: user = $user ? $user : user;
</script>

<svelte:head>
	<title>{user.name} Account Details | Meji</title>
</svelte:head>

<section class="details">
	<Card>
		<Title title="Account Details" />
		<Body>
			<div>
				<p>Account Balance: {currency(user.acc_balance)}</p>
			</div>
		</Body>
	</Card>

	<Card>
		<Body>
			<Button
				name="Add Voucher"
				on:click={() => {
					$module = {
						module: Add
					};
				}}
			/>
		</Body>
	</Card>
</section>

<style>
	.details {
		gap: var(--gap1);
		display: flex;
		flex-direction: column;
	}

	@media screen and (min-width: 800px) {
		.details {
			flex-direction: unset;
			/* flex-direction: row-reverse; */
			position: relative;
		}
	}
</style>
