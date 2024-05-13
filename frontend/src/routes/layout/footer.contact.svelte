<script>
	import Button from '$lib/button/button.svelte';
	import SVG from '$lib/svg.svelte';
</script>

<div class="block">
	<a href="tel:+2349113717298">
		<SVG icon="phone" />
		+234 911 371 7298
	</a>
	<a href="mailto:hello.meji@outlook.com">
		<SVG icon="email" />
		hello.meji@outlook.com
	</a>
	<a
		href="https://www.google.com/maps/place/Igando+Bus+Stop/@6.5513295,3.2380606,17z/data=!3m1!4b1!4m5!3m4!1s0x103b8540d0692809:0x4a45a882b29213a8!8m2!3d6.5513242!4d3.2402439"
		target="blank"
	>
		<SVG icon="location" />
		Lagos, Nigeria.
	</a>
</div>

<style>
	a {
		display: flex;
		align-items: center;
		gap: var(--sp1);

		width: fit-content;

		color: var(--ac2);
		fill: currentColor;
		text-decoration: none;
	}

	:hover {
		color: var(--cl1);
	}
</style>
