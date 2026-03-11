<script>
	let { label, href, receiver } = $props();
</script>

<hr style="border-color: gray; margin: 24px 0;" />

<b style="font-size: 0.8rem;">{label} </b>

{#if href}
	|
	<a style="text-decoration: none; color: #1d9bf0; font-size: 0.8rem;" {href} target="_blank">
		View Profile
	</a>
{/if}

<br />
<br />
Name: {receiver.name} <br />
{#if receiver.phone}
	Phone: {receiver.phone} <br />
{/if}
Email: {receiver.email} <br />
{#if receiver.address}
	Address: {receiver.address.address},
	{receiver.address.state},
	{receiver.address.country}
	{#if receiver.address.postal_code}
		<br />
		Postal Code: {receiver.address.postal_code}
	{/if}
{/if}
